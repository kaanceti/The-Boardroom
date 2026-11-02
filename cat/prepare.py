"""Build the office cat's training text: its starter voice, plus what it overhears in your meetings.

    python cat/prepare.py                 # starter voice + your meetings in data/meetings
    python cat/prepare.py --starter-only  # starter voice + the public example meetings only (safe to share)

Writes data/cat/corpus.txt and data/cat/memory.json. Both stay on your computer: data/ is never published.
Anything that sounds like advice, violence, and swearing are left out (see cat/safety.py),
so the cat never learns to sound like an adviser.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import safety  # noqa: E402
import voice  # noqa: E402

OUT = ROOT / "data" / "cat"
TEACHER = HERE / "teacher"   # several hundred original lines written for the cat by Claude, acting as its teacher


def teacher_lines():
    """Free lines, topic templates ({t}) and member templates ({m}) from cat/teacher/*.txt."""
    free, topics, members = [], [], []
    for f in sorted(TEACHER.glob("*.txt")) if TEACHER.exists() else []:
        if f.name.startswith(("wishes", "chat")):
            continue   # wishes have their own page in the cat's notebook (wish_lines); chat.txt is what people say to it (chat_groups)
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            (topics if "{t}" in line else members if "{m}" in line else free).append(line)
    return free, topics, members
ALLOWED = set("abcdefghijklmnopqrstuvwxyz0123456789 .,?!'\"-:;()%£*")
LEADS = ["could you please", "can you please", "should i", "should we", "why did", "why does", "why is", "why are", "why",
         "could you", "can you", "will", "does", "do", "is", "are", "how do i", "how can i", "how do", "what is",
         "what are", "what", "i want to", "i'd like to", "help me", "make me", "please", "tell me",
         "a friend wants to", "my friend wants to", "my partner wants to", "we want to", "i need to", "i need",
         "i am thinking of", "i'm thinking of", "thinking of", "i run", "i have", "i am", "i'm"]


TRAILING = {"to", "in", "and", "a", "an", "the", "of", "for", "with", "my", "your", "or", "on", "at", "just", "is", "it", "me", "us"}


def wish_lines() -> list[str]:
    """The cat's wishes (cat/teacher/wishes.txt). Its notebook asks for a line starting "i wish", "i want" and so on."""
    f = TEACHER / "wishes.txt"
    return [x.strip() for x in f.read_text(encoding="utf-8").splitlines() if x.strip()] if f.exists() else []


def chat_groups() -> list[tuple[list[str], list[str]]]:
    """What people say to the cat and its answers (cat/teacher/chat.txt): "## group", "> what a person types", "- an answer"."""
    f, groups = TEACHER / "chat.txt", []
    for line in f.read_text(encoding="utf-8").splitlines() if f.exists() else []:
        if line.startswith("## "):
            groups.append(([], []))
        elif line.startswith("> ") and groups:
            groups[-1][0].append(line[2:].strip())
        elif line.startswith("- ") and groups:
            groups[-1][1].append(line[2:].strip())
    return [g for g in groups if g[0] and g[1]]


def you_text(text: str, limit: int = 60) -> str:
    """What you typed, as the cat reads it: cleaned up and short enough to leave room for its answer. Same as catYou() in the page."""
    t = clean(text, markdown=False)
    if len(t) > limit:
        t = t[:limit].rsplit(" ", 1)[0]
    return t


# How people type: with or without its name, shorthand, and any punctuation.
_SHORT = [(r"\byou're\b", "ur"), (r"\byou\b", "u"), (r"\bare\b", "r"), (r"\bi'm\b", "im"), (r"\bwhat's\b", "whats"), (r"\byour\b", "ur")]
YOU_TOPIC = ["{t}", "{t}?", "{t}!", "what do you think of {t}?", "what do you think about {t}", "what about {t}?", "how was {t}?",
             "tell me about {t}", "kibi, {t}?", "i love {t}", "i hate {t}", "do you like {t}?", "we talked about {t} today",
             "any thoughts on {t}?", "have you heard of {t}?", "how do you feel about {t}?", "do you remember {t}?",
             "thoughts on {t}?", "i went to {t}", "hey kibi, what about {t}?", "{t} is tomorrow", "so, {t}"]


def typed(rng: random.Random, phrase: str) -> str:
    p = phrase.lower()
    r = rng.random()
    if r < .12:
        p = f"kibi, {p}"
    elif r < .2:
        p = f"hey kibi, {p}"
    elif r < .3:
        p = f"{p.rstrip('?!.')} kibi"
    if rng.random() < .12:
        for a, b in _SHORT:
            p = re.sub(a, b, p)
    end = rng.random()
    p = p.rstrip("?!.") + ("" if end < .4 else "?" if end < .7 and not p.endswith("!") else "!" if end < .8 else "." if end < .85 else p[-1] if p[-1] in "?!." else "")
    return you_text(p)


def chat_records(rng: random.Random, topic_templates: list[str], copy_templates: list[str], topics: list[str], per_phrase: int = 5) -> list[str]:
    """Things said to the cat in its notebook ("you: ...") and its answer, plus topics asked about in many ways.
    Many ways of saying each thing, a few times each: variety teaches it more than repeats do."""
    recs = []
    for phrases, answers in chat_groups():
        for phrase in phrases:
            for _ in range(per_phrase):
                answer = rng.choice(answers)
                recs.append(f"you: {typed(rng, phrase)}\ncat: {say(rng, answer) if rng.random() < .5 else clean(answer, markdown=False)}")
    for t in topics:
        asked = you_text(rng.choice(YOU_TOPIC).format(t=t))
        if t not in asked:
            continue
        recs.append(f"you: {asked}\ncat: {say(rng, rng.choice(copy_templates if rng.random() < .6 else topic_templates), t=t)}")
    return recs


def clean(text: str, markdown: bool = True) -> str:
    """Lower case, plain punctuation, no markdown, nothing the cat cannot spell."""
    text = unicodedata.normalize("NFKD", text)   # café becomes cafe (the accent is dropped below)
    text = text.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[–—]", "-", text)
    # Money signs the cat cannot spell become words: "£5" is "5 pounds", "20%" is "20 percent".
    text = re.sub(r"£\s?(\d[\d,.]*)", r"\1 pounds", text)
    text = re.sub(r"\$\s?(\d[\d,.]*)", r"\1 dollars", text)
    text = re.sub(r"€\s?(\d[\d,.]*)", r"\1 euros", text)
    text = text.replace("%", " percent").replace("£", " pounds")
    if markdown:
        text = re.sub(r"[#*_`|>\[\]]+", " ", text)
    text = "".join(c for c in text if c in ALLOWED or c == "\n")
    return re.sub(r"[ \t]+", " ", text).strip()


def topic_of(agenda: str) -> str:
    """'Why did Google miss earnings?' becomes 'google miss earnings'."""
    first = clean(agenda.strip().splitlines()[0] if agenda.strip() else "")
    first = re.split(r"[.?!,;]| because | so that | but ", first)[0].strip(" ,;:-\"'")
    for lead in sorted(LEADS, key=len, reverse=True):
        if first.startswith(lead + " "):
            first = first[len(lead) + 1:]
            break
    words = first.split()[:5]
    while words and words[-1] in TRAILING:
        words.pop()
    return " ".join(words).strip(" ,;:-\"'")


def sentences(text: str) -> list[str]:
    out = []
    for line in clean(text).splitlines():
        line = line.strip(" -:")
        if line.startswith(("verdict", "bottom line", "none")):
            continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if 20 <= len(s) <= 160 and not s.startswith(("http", "statement ")):
                out.append(s)
    return out


def quotes(sents: list[str], rng: random.Random, n: int) -> list[str]:
    """Short snippets the cat can repeat back: whole short sentences, or the start of one (easier to say well)."""
    found = []
    for s in sents:
        words = re.sub(r"[\"()]", "", s).rstrip(".!?").split()
        if 3 <= len(words) <= 7:
            found.append(" ".join(words))
        elif len(words) > 7:
            found.append(" ".join(words[:rng.randint(4, 6)]).strip(" ,;:"))
    rng.shuffle(found)
    return [q for q in found if len(q) > 8][:n]


def say(rng: random.Random, template: str, **slots) -> str:
    """One cat line. Long ones lose their extras, so a topic and the line fit in what the cat can hold in mind."""
    core = template.format(**slots)
    opener, closer = rng.choice(voice.OPENERS), rng.choice(voice.CLOSERS)
    if core.startswith("*"):
        opener = ""
    if "*" in core[1:]:
        closer = ""
    if len(core) + len(opener) + len(closer) > 95:
        closer = ""
    if len(core) + len(opener) > 95:
        opener = ""
    return clean(" ".join(x for x in (opener, core, closer) if x), markdown=False)


def meeting_text(m: dict) -> str:
    parts = [s.get("text") or "" for s in m.get("statements") or []]
    parts += [r.get("text") or "" for r in m.get("reviews") or []]
    parts.append((m.get("resolution") or {}).get("text") or "")
    return "\n".join(parts)


def records_for_meeting(m: dict, rng: random.Random, members: list[str], weight: int,
                        topic_templates: list[str] | None = None, member_templates: list[str] | None = None) -> tuple[list[str], dict]:
    topic = topic_of(m.get("agenda", ""))
    usable = bool(topic) and safety.safe(topic)    # a topic with swearing or violence is never repeated
    sents = [s for s in sentences(meeting_text(m)) if safety.safe(s)]
    names = [clean(n) for n in (m.get("names") or {}).values() if clean(n) and safety.safe(n)] or members
    recs = []
    if usable:
        templates = topic_templates or voice.TOPIC + voice.GENRE_TOPIC
        recs += [f"topic: {topic}\ncat: {say(rng, rng.choice(templates), t=topic)}" for _ in range(30 * weight)]
        for q in [q for q in quotes(sents, rng, 12 * weight) if safety.safe(q)][:5 * weight]:
            recs.append(f"topic: {topic}\ncat: {say(rng, rng.choice(voice.QUOTE), b=q)}")
        for _ in range(6 * weight):   # asked about in the notebook, too
            asked = you_text(rng.choice(YOU_TOPIC).format(t=topic))
            if topic in asked:
                recs.append(f"you: {asked}\ncat: {say(rng, rng.choice(templates), t=topic)}")
    recs += [f"cat: {say(rng, rng.choice(member_templates or voice.MEMBER), m=rng.choice(names))}" for _ in range(4 * weight)]
    # Enough of what the board said to learn its words, without drowning out the cat's own voice.
    rng.shuffle(sents)
    recs += [f"board: {s}" for s in sents[:60 * weight]]
    memory = {"id": m.get("id"), "when": (m.get("created") or "")[:10], "topic": topic, "usable": usable, "names": names}
    return recs, memory


def build(meeting_files: list[Path], extra_files: list[Path] = (), seed: int = 7, books: Path | None = None,
          book_share: float = 0.15) -> tuple[list[str], list[dict]]:
    rng = random.Random(seed)
    members = voice.STARTER_MEMBERS
    t_free, t_topics, t_members = teacher_lines()
    topic_templates = voice.TOPIC + voice.GENRE_TOPIC + t_topics
    member_templates = voice.MEMBER + t_members
    recs = []
    for t in voice.STARTER_TOPICS:
        recs += [f"topic: {t}\ncat: {say(rng, rng.choice(topic_templates), t=t)}" for _ in range(24)]
    recs += [f"cat: {say(rng, line)}" for line in voice.FREE + voice.GENRE + t_free for _ in range(6)]
    recs += [f"cat: {say(rng, rng.choice(member_templates), m=rng.choice(members))}" for _ in range(1500)]
    # Thousands of made-up topics, so it learns to repeat whatever topic it is given (what you type in its notebook).
    # Templates that say the topic early or twice give it the most practice at copying (cat/teacher/topics5.txt).
    copy_templates = [x for x in topic_templates if x.find("{t}") <= 3 or x.count("{t}") >= 2]
    for t in voice.random_topics(rng, 12000, invented_share=.35):
        recs.append(f"topic: {t}\ncat: {say(rng, rng.choice(copy_templates if rng.random() < .6 else topic_templates), t=t)}")
    # What people say to it in its notebook, and topics asked about the way people ask (cat/teacher/chat.txt).
    recs += chat_records(rng, topic_templates, copy_templates, voice.STARTER_TOPICS * 6 + voice.random_topics(rng, 5000, invented_share=.35))
    # Wishes, mostly with nothing in front, so a line that starts "i wish" carries on as a wish.
    wishes = wish_lines()
    recs += [f"cat: {clean(w, markdown=False)}" for w in wishes for _ in range(6)]
    recs += [f"cat: {say(rng, w)}" for w in wishes for _ in range(2)]
    memory = []
    # Newer meetings count more, so the cat talks about what you asked recently.
    for i, f in enumerate(sorted(meeting_files)):
        try:
            m = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if m.get("stage") != "done":
            continue
        r, mem = records_for_meeting(m, rng, members, 2 if i >= len(meeting_files) - 5 else 1, topic_templates, member_templates)
        recs += r
        memory.append(mem)
    # The example meetings that ship with the app widen its vocabulary, but it does not "remember" them.
    for f in extra_files:
        try:
            m = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        recs += records_for_meeting(m, rng, members, 1, topic_templates, member_templates)[0]
    # Old public-domain stories teach it English, kept to a small share so the cat's own voice stays in charge.
    if books and books.exists():
        story = [s for s in books.read_text(encoding="utf-8").splitlines() if s.strip()]
        rng.shuffle(story)
        budget, used = book_share / (1 - book_share) * sum(len(r) for r in recs), 0
        for s in story:
            if used >= budget:
                break
            recs.append(f"story: {s}")
            used += len(s) + 7
    # Last check on every line, whatever its source.
    recs = [r for r in recs if safety.safe(r)]
    rng.shuffle(recs)
    return recs, memory


def real_words(text: str, least: int = 2) -> set[str]:
    """The words the cat may write (tinycat.py say): every word in its lessons read at least twice, since once could be a typo.
    The made-up practice topics are taken out by run(), so it cannot drift into "nutipok" on its own."""
    seen = {}
    for w in re.findall(r"[a-z']+", text):
        w = w.strip("'")
        if w:
            seen[w] = seen.get(w, 0) + 1
    return {w for w, n in seen.items() if n >= least}


def run(meetings: Path | None = None, examples: Path | None = None, out: Path = OUT, starter_only: bool = False,
        books: Path | None = None):
    """Write corpus.txt, words.txt and memory.json. Used by the command line below and by the app after each meeting."""
    examples = examples or ROOT / "benchmark" / "meetings"
    meetings = meetings or ROOT / "data" / "meetings"
    files = [] if starter_only else sorted(meetings.glob("*.json")) if meetings.exists() else []
    extra = sorted(examples.glob("*.json")) if examples.exists() else []
    voice.MADE_UP.clear()
    recs, memory = build(files, extra, books=books)
    out.mkdir(parents=True, exist_ok=True)
    text = "\n\n".join(recs) + "\n\n"
    (out / "corpus.txt").write_text(text, encoding="utf-8")
    # Made-up practice words come off the list, unless a real lesson uses the same word ("kibi", "papa").
    trusted = " ".join(f.read_text(encoding="utf-8") for f in TEACHER.glob("*.txt")) + Path(voice.__file__).read_text(encoding="utf-8")
    trusted += " ".join(r for r in recs if r.startswith(("story:", "board:")))
    fake = voice.MADE_UP - set(re.findall(r"[a-z']+", trusted.lower()))
    (out / "words.txt").write_text("\n".join(sorted(real_words(text) - fake)) + "\n", encoding="utf-8")
    (out / "memory.json").write_text(json.dumps(memory, indent=1, ensure_ascii=False), encoding="utf-8")
    return recs, memory


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--starter-only", action="store_true", help="use the public example meetings instead of yours")
    ap.add_argument("--meetings", type=Path, help="folder of meeting .json files (default: data/meetings)")
    ap.add_argument("--examples", type=Path, help="public example meetings (default: benchmark/meetings)")
    ap.add_argument("--books", type=Path, help="one sentence per line of public-domain stories (see repo-tools/books.py)")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    recs, memory = run(args.meetings, args.examples, args.out, args.starter_only, args.books)
    size = sum(len(r) for r in recs)
    print(f"{len(recs)} lines ({size // 1000} KB) from {len(memory)} meetings -> {args.out / 'corpus.txt'}")
    for mem in memory[-5:]:
        print(f"  remembers: {mem['when']}  {mem['topic'] if mem['usable'] else '(a topic it will not repeat)'}")


if __name__ == "__main__":
    main()
