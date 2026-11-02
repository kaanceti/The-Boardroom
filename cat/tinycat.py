"""TinyCat: a very small language model, written from scratch with nothing but NumPy.

It reads text one letter at a time and learns to guess the next letter. That is all a large language
model does too; this one just has about a million numbers to learn with instead of billions.

    python cat/tinycat.py train                 # learn from data/cat/corpus.txt (keeps learning if a brain exists)
    python cat/tinycat.py train --fresh         # forget everything and start again
    python cat/tinycat.py say --topic "the café" -n 5
    python cat/tinycat.py export                # write data/cat/brain.json for the app

The brain is saved in data/cat/, next to your meetings, and is never published.
"""
import argparse
import base64
import json
import math
import multiprocessing as mp
import os
import re
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "cat"
STARTER = HERE / "starter-brain.npz"   # trained only on the starter lines and the public example meetings
F = np.float32
SIZES = dict(context=128, width=128, layers=4, heads=4)


# ---------------------------------------------------------------- the model
def init(vocab: int, context: int, width: int, layers: int, heads: int, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    n = lambda *shape, s=0.02: (rng.standard_normal(shape) * s).astype(F)
    deep = 0.02 / math.sqrt(2 * layers)   # keep the residual stream calm as layers add up
    p = {"wte": n(vocab, width), "wpe": n(context, width), "lnf_g": np.ones(width, F), "lnf_b": np.zeros(width, F)}
    for i in range(layers):
        p.update({f"{i}.ln1_g": np.ones(width, F), f"{i}.ln1_b": np.zeros(width, F),
                  f"{i}.w_qkv": n(width, 3 * width), f"{i}.b_qkv": np.zeros(3 * width, F),
                  f"{i}.w_o": n(width, width, s=deep), f"{i}.b_o": np.zeros(width, F),
                  f"{i}.ln2_g": np.ones(width, F), f"{i}.ln2_b": np.zeros(width, F),
                  f"{i}.w_fc": n(width, 4 * width), f"{i}.b_fc": np.zeros(4 * width, F),
                  f"{i}.w_pr": n(4 * width, width, s=deep), f"{i}.b_pr": np.zeros(width, F)})
    return p


def ln_fwd(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = x.var(-1, keepdims=True)
    inv = 1.0 / np.sqrt(var + eps)
    xh = (x - mu) * inv
    return xh * g + b, (xh, inv, g)


def ln_bwd(dy, cache):
    xh, inv, g = cache
    dxh = dy * g
    dx = inv * (dxh - dxh.mean(-1, keepdims=True) - xh * (dxh * xh).mean(-1, keepdims=True))
    red = tuple(range(dy.ndim - 1))
    return dx, (dy * xh).sum(red), dy.sum(red)


C0 = math.sqrt(2 / math.pi)


def gelu(x):
    t = np.tanh(C0 * (x + 0.044715 * x ** 3))
    return 0.5 * x * (1 + t), t


def gelu_bwd(x, t):
    return 0.5 * (1 + t) + 0.5 * x * (1 - t * t) * C0 * (1 + 3 * 0.044715 * x * x)


def forward(p: dict, idx: np.ndarray, cfg: dict, targets=None):
    B, T = idx.shape
    H, C = cfg["heads"], cfg["width"]
    hd = C // H
    mask = np.tril(np.ones((T, T), bool))
    x = p["wte"][idx] + p["wpe"][:T]
    caches = []
    for i in range(cfg["layers"]):
        h1, c1 = ln_fwd(x, p[f"{i}.ln1_g"], p[f"{i}.ln1_b"])
        qkv = h1 @ p[f"{i}.w_qkv"] + p[f"{i}.b_qkv"]
        q, k, v = (a.reshape(B, T, H, hd).transpose(0, 2, 1, 3) for a in np.split(qkv, 3, axis=-1))
        att = (q @ k.transpose(0, 1, 3, 2)) / math.sqrt(hd)
        att = np.where(mask, att, F(-1e9))
        att = np.exp(att - att.max(-1, keepdims=True))
        pr = att / att.sum(-1, keepdims=True)
        y = (pr @ v).transpose(0, 2, 1, 3).reshape(B, T, C)
        x = x + y @ p[f"{i}.w_o"] + p[f"{i}.b_o"]
        h2, c2 = ln_fwd(x, p[f"{i}.ln2_g"], p[f"{i}.ln2_b"])
        f = h2 @ p[f"{i}.w_fc"] + p[f"{i}.b_fc"]
        g, t = gelu(f)
        x = x + g @ p[f"{i}.w_pr"] + p[f"{i}.b_pr"]
        caches.append((h1, c1, q, k, v, pr, y, h2, c2, f, g, t))
    hf, cf = ln_fwd(x, p["lnf_g"], p["lnf_b"])
    logits = hf @ p["wte"].T                     # the output layer reuses the letter table
    if targets is None:
        return logits
    z = logits - logits.max(-1, keepdims=True)
    probs = np.exp(z)
    probs /= probs.sum(-1, keepdims=True)
    n = B * T
    loss = -np.log(probs.reshape(n, -1)[np.arange(n), targets.reshape(n)] + 1e-9).mean()
    return loss, (idx, targets, probs, hf, cf, caches)


def backward(p: dict, cache, cfg: dict) -> dict:
    idx, targets, probs, hf, cf, caches = cache
    B, T = idx.shape
    H, C = cfg["heads"], cfg["width"]
    hd = C // H
    V = p["wte"].shape[0]
    gr = {k: np.zeros_like(v) for k, v in p.items()}
    dlog = probs.copy()
    dlog.reshape(B * T, V)[np.arange(B * T), targets.reshape(-1)] -= 1
    dlog /= B * T
    gr["wte"] += dlog.reshape(-1, V).T @ hf.reshape(-1, C)
    dx, gr["lnf_g"], gr["lnf_b"] = ln_bwd(dlog @ p["wte"], cf)
    for i in reversed(range(cfg["layers"])):
        h1, c1, q, k, v, pr, y, h2, c2, f, g, t = caches[i]
        gr[f"{i}.w_pr"] = g.reshape(-1, 4 * C).T @ dx.reshape(-1, C)
        gr[f"{i}.b_pr"] = dx.sum((0, 1))
        df = (dx @ p[f"{i}.w_pr"].T) * gelu_bwd(f, t)
        gr[f"{i}.w_fc"] = h2.reshape(-1, C).T @ df.reshape(-1, 4 * C)
        gr[f"{i}.b_fc"] = df.sum((0, 1))
        d, gr[f"{i}.ln2_g"], gr[f"{i}.ln2_b"] = ln_bwd(df @ p[f"{i}.w_fc"].T, c2)
        dx = dx + d
        gr[f"{i}.w_o"] = y.reshape(-1, C).T @ dx.reshape(-1, C)
        gr[f"{i}.b_o"] = dx.sum((0, 1))
        dy = (dx @ p[f"{i}.w_o"].T).reshape(B, T, H, hd).transpose(0, 2, 1, 3)
        dpr = dy @ v.transpose(0, 1, 3, 2)
        dv = pr.transpose(0, 1, 3, 2) @ dy
        datt = pr * (dpr - (dpr * pr).sum(-1, keepdims=True)) / math.sqrt(hd)
        dq = datt @ k
        dk = datt.transpose(0, 1, 3, 2) @ q
        dqkv = np.concatenate([a.transpose(0, 2, 1, 3).reshape(B, T, C) for a in (dq, dk, dv)], axis=-1)
        gr[f"{i}.w_qkv"] = h1.reshape(-1, C).T @ dqkv.reshape(-1, 3 * C)
        gr[f"{i}.b_qkv"] = dqkv.sum((0, 1))
        d, gr[f"{i}.ln1_g"], gr[f"{i}.ln1_b"] = ln_bwd(dqkv @ p[f"{i}.w_qkv"].T, c1)
        dx = dx + d
    onehot = np.zeros((B * T, V), F)
    onehot[np.arange(B * T), idx.reshape(-1)] = 1
    gr["wte"] += onehot.T @ dx.reshape(-1, C)
    gr["wpe"][:T] += dx.sum(0)
    return gr


# ---------------------------------------------------------------- saving and loading
def save(path: Path, p: dict, cfg: dict, vocab: str, steps: int, words: list[str] | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = json.dumps({**cfg, "vocab": vocab, "steps": steps, "saved": time.strftime("%Y-%m-%d %H:%M"), "words": words or []})
    np.savez(path, __meta__=np.frombuffer(meta.encode(), np.uint8), **p)


def load(path: Path):
    z = np.load(path)
    meta = json.loads(bytes(z["__meta__"]).decode())
    p = {k: z[k].astype(F) for k in z.files if k != "__meta__"}
    cfg = {k: meta[k] for k in SIZES}
    return p, cfg, meta["vocab"], meta.get("steps", 0)


def load_words(path: Path) -> list[str]:
    """The real words the brain has read, kept with it so it can write only those (see say)."""
    return json.loads(bytes(np.load(path)["__meta__"]).decode()).get("words", [])


def count_words(text: str, least: int = 2) -> set[str]:
    """Words in the training text, if prepare.py did not write a words.txt. Read once could be a typo, so twice counts."""
    seen = {}
    for w in re.findall(r"[a-z']+", text):
        w = w.strip("'")
        if w:
            seen[w] = seen.get(w, 0) + 1
    return {w for w, n in seen.items() if n >= least}


# ---------------------------------------------------------------- learning
def batches(text: str, vocab: str, cfg: dict, batch: int, rng):
    lut = {c: i for i, c in enumerate(vocab)}
    data = np.array([lut.get(c, lut[" "]) for c in text], np.int64)
    starts = np.array([0] + [mt.end() for mt in re.finditer("\n\n", text)])
    starts = starts[starts < len(data) - cfg["context"] - 1]
    T = cfg["context"]
    while True:
        s = rng.choice(starts, batch)
        win = np.stack([data[i:i + T + 1] for i in s])
        yield win[:, :-1], win[:, 1:]


_W = {}


def _helper_start(text, vocab, cfg, batch, seed):
    """A helper process (--workers): its own stream of training snippets."""
    _W["cfg"] = cfg
    _W["batches"] = batches(text, vocab, cfg, batch, np.random.default_rng([seed, os.getpid()]))


def _helper_grad(p):
    x, y = next(_W["batches"])
    loss, cache = forward(p, x, _W["cfg"], y)
    return loss, backward(p, cache, _W["cfg"])


def train(args):
    corpus = args.corpus or DATA / "corpus.txt"
    text = corpus.read_text(encoding="utf-8")
    brain = args.brain
    if not brain.exists() and not args.fresh and STARTER.exists():
        brain.parent.mkdir(parents=True, exist_ok=True)
        brain.write_bytes(STARTER.read_bytes())
        print("Starting from the starter brain.")
    fresh = args.fresh or not brain.exists()
    lr_peak = args.lr or (2e-3 if fresh else 5e-4)   # gentler when it already knows things, so it does not forget them
    if not fresh:
        p, cfg, vocab, done = load(brain)
        extra = sorted(set(text) - set(vocab))
        if extra:   # new letters showed up in your meetings: give them fresh rows
            rng0 = np.random.default_rng(done)
            p["wte"] = np.concatenate([p["wte"], (rng0.standard_normal((len(extra), cfg["width"])) * 0.02).astype(F)])
            vocab += "".join(extra)
        print(f"Keeping learning from step {done} ({len(vocab)} letters).")
    else:
        vocab = "".join(sorted(set(text) | set(" \n")))
        cfg = dict(SIZES)
        for k in SIZES:   # a new brain can be bigger or smaller than the default
            if getattr(args, k, None):
                cfg[k] = getattr(args, k)
        p, done = init(len(vocab), **cfg), 0
        print(f"New brain: {sum(v.size for v in p.values()):,} numbers to learn, {len(vocab)} letters.")
    # The real words it has read so far (prepare.py lists them, made-up practice topics left out), so it can write only those.
    wf = corpus.with_name("words.txt")
    words = set(wf.read_text(encoding="utf-8").split()) if wf.exists() else count_words(text)
    words = sorted(words | set(load_words(brain) if not fresh else []))
    cut = int(len(text) * .95)
    cut = text.find("\n\n", cut) + 2
    rng = np.random.default_rng(done + 1)
    train_b = batches(text[:cut], vocab, cfg, args.batch, rng)
    val_b = batches(text[cut:], vocab, cfg, args.batch, np.random.default_rng(0))
    names = list(p)
    # Extra processor cores each read their own snippets; their lessons are averaged into one step.
    workers = max(1, getattr(args, "workers", 1) or 1)
    pool = mp.get_context("spawn").Pool(workers - 1, _helper_start, (text[:cut], vocab, cfg, args.batch, done + 1)) if workers > 1 else None
    m = {k: np.zeros_like(v) for k, v in p.items()}
    v2 = {k: np.zeros_like(v) for k, v in p.items()}
    t0, steps = time.time(), args.steps
    for step in range(1, steps + 1):
        # warm up, then ease the learning rate down so it settles
        lr = lr_peak * min(1, step / 100) * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * step / steps)))
        jobs = [pool.apply_async(_helper_grad, (p,)) for _ in range(workers - 1)] if pool else []
        x, y = next(train_b)
        loss, cache = forward(p, x, cfg, y)
        gr = backward(p, cache, cfg)
        for job in jobs:
            l2, g2 = job.get()
            loss += l2
            for k in names:
                gr[k] += g2[k]
        if jobs:
            loss /= workers
            for k in names:
                gr[k] /= workers
        norm = math.sqrt(sum(float((g * g).sum()) for g in gr.values()))
        scale = min(1.0, 1.0 / (norm + 1e-6))
        for k in names:
            g = gr[k] * scale
            m[k] = 0.9 * m[k] + 0.1 * g
            v2[k] = 0.99 * v2[k] + 0.01 * g * g
            mh, vh = m[k] / (1 - 0.9 ** step), v2[k] / (1 - 0.99 ** step)
            decay = lr * 0.01 * p[k] if p[k].ndim == 2 else 0
            p[k] -= (lr * mh / (np.sqrt(vh) + 1e-8) + decay).astype(F)
        if step % 10 == 0:
            print(f"progress {step}/{steps}", flush=True)
        if step % args.every == 0 or step == steps:
            vloss = sum(forward(p, vx, cfg, vy)[0] for vx, vy in (next(val_b) for _ in range(8))) / 8   # one batch alone is too noisy
            rate = step / (time.time() - t0)
            print(f"step {done + step:5d}  loss {loss:.3f}  check {vloss:.3f}  ({rate:.1f} steps/s)", flush=True)
            print("   cat:", say(p, cfg, vocab, rng, topic=args.peek)[0], flush=True)
            save(brain, p, cfg, vocab, done + step, words)
    save(brain, p, cfg, vocab, done + steps, words)
    if pool:
        pool.close()
    print(f"Saved {brain}")


# ---------------------------------------------------------------- talking
END = "END"
WORD = re.compile(r"[a-z0-9'-]")   # after a finished topic, a hyphen would glue on another word ("the bake sale-took")


def copy_next(out: str, topic: str | None, start_after: int = 3, started: bool = False) -> str | None:
    """Spelling help: once the cat has started writing its topic (three letters past "the", "my" or "a"),
    the next letter of the topic is chosen for it, so names come out whole instead of half-remembered.
    Once the whole topic is written it may not run on into a longer word: END asks for a letter that ends the word."""
    if not topic:
        return None
    lead = next((w for w in ("the ", "my ", "a ", "an ") if topic.startswith(w)), "")

    def starts(m):
        return out.endswith(topic[:m]) and (len(out) == m or not out[-m - 1].isalpha())
    if starts(len(topic)):
        return END
    if topic in out:
        return None   # help with the topic once per line, so it does not take over every word
    # A topic with no "the" in front needs three letters of its own first ("tru" for "trump"), or every t-word would turn into it.
    for m in range(len(topic) - 1, (len(lead) + start_after if lead else 1 if started else max(start_after, 3)) - 1, -1):
        if starts(m):
            return topic[m]
    return None


LETTERS = set("abcdefghijklmnopqrstuvwxyz'")


def spell_mask(out: str, vocab: str, words: set, prefixes: set, extra: set) -> np.ndarray:
    """Real words only: which letters may come next so the word being written stays on its way to a word the cat has read
    (or one in your message or topic), and a word may only end once it is a whole word. Same as allowed() in tinycat.js."""
    part = re.search(r"[a-z']*$", out).group(0)

    def is_prefix(s):
        return s in prefixes or any(w.startswith(s) for w in extra)
    whole = part == "" or part in words or part in extra
    return np.array([is_prefix(part + c) if c in LETTERS else whole for c in vocab])


def say(p, cfg, vocab, rng, topic=None, n=1, temperature=0.8, top_k=12, start="", copy=True, copy_from=0, you=None, words=None):
    """Lines from the cat. you: what someone typed to it (it answers that); topic: what to talk about, and the word it gets
    spelling help with. words: the real words it has read; given, it writes only those (no half-made words like "saleep")."""
    lut = {c: i for i, c in enumerate(vocab)}
    words = set(words or ())
    prefixes = {w[:i] for w in words for i in range(1, len(w) + 1)}
    extra = set(re.findall(r"[a-z']+", " ".join(x.lower() for x in (topic, you, start) if x)))
    topic = topic.lower() if topic else None
    start = start.lower().strip()
    head = f"you: {you.lower()}\n" if you else f"topic: {topic}\n" if topic else ""
    prompt = head + "cat:" + (f" {start}" if start else "")
    lines = []
    for _ in range(n):
        ids = [lut[c] for c in prompt if c in lut]
        out = start
        started = False   # set once the cat has been helped to start its topic, so it can finish it
        for _ in range(110):
            ctx = np.array([ids[-cfg["context"]:]])
            logits = forward(p, ctx, cfg)[0, -1] / temperature
            top = np.argsort(logits)[-top_k:]
            mask = spell_mask(out, vocab, words, prefixes, extra) if words else None
            pool = np.where(mask, logits, -np.inf) if mask is not None and mask.any() else logits
            choose = np.argsort(pool)[-top_k:]
            w = np.exp(pool[choose] - pool[choose].max())
            nxt = int(rng.choice(choose, p=w / w.sum()))
            forced = copy_next(out, topic, 1 if started else max(copy_from, 1), started) if copy else None
            if copy and copy_from == 0 and forced is None and topic and topic not in out:
                # Start the topic where a topic usually goes, if its first letter is one the cat was already considering:
                # right after "the", "my" or "a" for "the zumba class", at the start of a sentence for a bare word like "glimbo".
                lead = next((w for w in ("the ", "my ", "a ", "an ") if topic.startswith(w)), "")
                if lead:
                    at = out.endswith(lead) and (len(out) == len(lead) or not out[-len(lead) - 1].isalpha())
                else:
                    at = out.strip() == "" or re.search(r"[.?!] $", out) is not None
                if at and lut.get(topic[len(lead)]) in set(top.tolist()):
                    forced, started = topic[len(lead)], True
            if forced == END:
                if WORD.match(vocab[nxt]):
                    ok = [i for i, c in enumerate(vocab) if not WORD.match(c) and not (c == "\n" and len(out) < 30)]
                    nxt = max(ok, key=lambda i: logits[i])
            elif forced in lut:
                nxt = lut[forced]
            if vocab[nxt] == "\n":
                break
            ids.append(nxt)
            out += vocab[nxt]
        lines.append(out.strip())
    return lines


def export(args):
    """Write the brain as JSON so the app can run it in the browser, no Python needed.
    Numbers are stored at half precision, which halves the file and changes nothing you would notice."""
    p, cfg, vocab, steps = load(args.brain)
    arr = {k: {"shape": list(v.shape), "data": base64.b64encode(v.astype("<f2").tobytes()).decode()} for k, v in p.items()}
    out = args.out or args.brain.with_suffix(".json")
    out.write_text(json.dumps({**cfg, "vocab": vocab, "steps": steps, "dtype": "f16", "words": load_words(args.brain), "weights": arr}),
                   encoding="utf-8")
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["train", "say", "export"])
    ap.add_argument("--brain", type=Path, default=DATA / "brain.npz")
    ap.add_argument("--corpus", type=Path)
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--batch", type=int, default=24)
    ap.add_argument("--workers", type=int, default=1, help="processor cores to train with (each reads its own snippets)")
    ap.add_argument("--lr", type=float, default=None, help="learning rate (default 0.002 new, 0.0005 when it keeps learning)")
    ap.add_argument("--out", type=Path, default=None, help="where export writes the JSON")
    ap.add_argument("--every", type=int, default=100)
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--width", type=int, help="new brains only: numbers per letter (default 128)")
    ap.add_argument("--layers", type=int, help="new brains only: transformer blocks (default 4)")
    ap.add_argument("--heads", type=int, help="new brains only: attention heads (default 4)")
    ap.add_argument("--context", type=int, help="new brains only: letters it can look back over (default 128)")
    ap.add_argument("--peek", default=None, help="topic to try while training")
    ap.add_argument("--topic", default=None)
    ap.add_argument("--you", default=None, help="something to say to the cat, as in its notebook")
    ap.add_argument("--start", default="", help="words the line must begin with, like \"i wish\"")
    ap.add_argument("-n", type=int, default=5)
    ap.add_argument("--temperature", type=float, default=0.8)
    args = ap.parse_args()
    if args.command == "train":
        train(args)
    elif args.command == "say":
        p, cfg, vocab, steps = load(args.brain)
        for line in say(p, cfg, vocab, np.random.default_rng(), topic=args.topic, n=args.n, temperature=args.temperature, start=args.start,
                        you=args.you, words=load_words(args.brain)):
            print("cat:", line)
    else:
        export(args)


if __name__ == "__main__":
    main()
