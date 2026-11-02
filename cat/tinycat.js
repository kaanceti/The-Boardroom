// TinyCat in the browser: runs the brain that cat/tinycat.py trained, with no libraries.
// It does the same maths as the Python version, one letter at a time, remembering earlier letters as it goes.
(function (root) {
  "use strict";

  function decode(b64, half) {
    const bin = atob(b64), bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    if (!half) return new Float32Array(bytes.buffer);
    // Half-precision numbers (16 bits each) back to normal ones.
    const h = new Uint16Array(bytes.buffer), out = new Float32Array(h.length);
    for (let i = 0; i < h.length; i++) {
      const s = h[i] & 0x8000 ? -1 : 1, e = (h[i] >> 10) & 0x1f, f = h[i] & 0x3ff;
      out[i] = e === 0 ? s * f * 5.960464477539063e-8 : e === 31 ? (f ? NaN : s * Infinity) : s * Math.pow(2, e - 15) * (1 + f / 1024);
    }
    return out;
  }

  // Spelling help, the same as copy_next in tinycat.py: once the cat has started writing its topic
  // (three letters past "the", "my" or "a"), the next letter of the topic is chosen for it.
  // Once the whole topic is written it may not run on into a longer word ("the bake saleng"): END asks for the
  // likeliest letter that is not part of a word.
  const END = "END";
  const LETTER = /[a-z']/;
  function copyNext(out, topic, from = 3, started = false) {
    if (!topic) return null;
    const lead = ["the ", "my ", "a ", "an "].find(w => topic.startsWith(w)) || "";
    const starts = m => out.endsWith(topic.slice(0, m)) && (out.length === m || !/[a-z]/.test(out[out.length - m - 1]));
    if (starts(topic.length)) return END;
    if (out.includes(topic)) return null;   // help with the topic once per line, so it does not take over every word
    // A topic with no "the" in front needs three letters of its own first ("tru" for "trump"), or every t-word would turn into it.
    for (let m = topic.length - 1; m >= (lead ? lead.length + from : started ? 1 : Math.max(from, 3)); m--) if (starts(m)) return topic[m];
    return null;
  }

  class TinyCat {
    constructor(brain) {
      this.T = brain.context; this.C = brain.width; this.L = brain.layers; this.H = brain.heads;
      this.vocab = brain.vocab; this.steps = brain.steps;
      this.lut = new Map([...this.vocab].map((c, i) => [c, i]));
      this.w = {};
      for (const [k, v] of Object.entries(brain.weights)) this.w[k] = decode(v.data, brain.dtype === "f16");
      this.V = this.vocab.length;
      // The real words it has read (saved with the brain), so it can write only those. Older brains have none: no limit.
      this.words = new Set(brain.words || []);
      this.prefixes = new Set();
      for (const w of this.words) for (let i = 1; i <= w.length; i++) this.prefixes.add(w.slice(0, i));
      this.reset();
    }

    // Real words only, the same as spell_mask in tinycat.py: which letters may come next so the word being written stays on its
    // way to a word the cat has read (or one in your message or topic), and a word may only end once it is a whole word.
    allowed(out, extra) {
      const part = out.match(/[a-z']*$/)[0];
      const isPrefix = s => this.prefixes.has(s) || extra.some(w => w.startsWith(s));
      const whole = part === "" || this.words.has(part) || extra.includes(part);
      return [...this.vocab].map(c => LETTER.test(c) ? isPrefix(part + c) : whole);
    }

    reset() {
      const { T, C, L } = this;
      this.keys = Array.from({ length: L }, () => new Float32Array(T * C));
      this.vals = Array.from({ length: L }, () => new Float32Array(T * C));
      this.pos = 0;
    }

    // y = x W + b, with W stored row by row as (rows x cols)
    affine(x, W, b, cols) {
      const y = new Float32Array(cols);
      if (b) y.set(b);
      for (let i = 0; i < x.length; i++) {
        const xi = x[i], row = i * cols;
        if (xi === 0) continue;
        for (let j = 0; j < cols; j++) y[j] += xi * W[row + j];
      }
      return y;
    }

    norm(x, g, b) {
      let mu = 0, v = 0;
      for (const a of x) mu += a;
      mu /= x.length;
      for (const a of x) v += (a - mu) * (a - mu);
      const inv = 1 / Math.sqrt(v / x.length + 1e-5), y = new Float32Array(x.length);
      for (let i = 0; i < x.length; i++) y[i] = (x[i] - mu) * inv * g[i] + b[i];
      return y;
    }

    // Feed one letter; get back a score for every possible next letter.
    step(id) {
      const { C, H, w } = this, hd = C / H, t = this.pos;
      const x = new Float32Array(C);
      for (let i = 0; i < C; i++) x[i] = w.wte[id * C + i] + w.wpe[t * C + i];
      for (let l = 0; l < this.L; l++) {
        const h = this.norm(x, w[`${l}.ln1_g`], w[`${l}.ln1_b`]);
        const qkv = this.affine(h, w[`${l}.w_qkv`], w[`${l}.b_qkv`], 3 * C);
        this.keys[l].set(qkv.subarray(C, 2 * C), t * C);
        this.vals[l].set(qkv.subarray(2 * C), t * C);
        const y = new Float32Array(C), scale = 1 / Math.sqrt(hd), sc = new Float32Array(t + 1);
        for (let hh = 0; hh < H; hh++) {
          const o = hh * hd;
          let mx = -Infinity;
          for (let s = 0; s <= t; s++) {
            let d = 0;
            for (let i = 0; i < hd; i++) d += qkv[o + i] * this.keys[l][s * C + o + i];
            sc[s] = d * scale;
            if (sc[s] > mx) mx = sc[s];
          }
          let sum = 0;
          for (let s = 0; s <= t; s++) { sc[s] = Math.exp(sc[s] - mx); sum += sc[s]; }
          for (let s = 0; s <= t; s++) {
            const p = sc[s] / sum;
            for (let i = 0; i < hd; i++) y[o + i] += p * this.vals[l][s * C + o + i];
          }
        }
        const a = this.affine(y, w[`${l}.w_o`], w[`${l}.b_o`], C);
        for (let i = 0; i < C; i++) x[i] += a[i];
        const h2 = this.norm(x, w[`${l}.ln2_g`], w[`${l}.ln2_b`]);
        const f = this.affine(h2, w[`${l}.w_fc`], w[`${l}.b_fc`], 4 * C);
        for (let i = 0; i < f.length; i++) {
          const u = f[i];
          f[i] = 0.5 * u * (1 + Math.tanh(0.7978845608028654 * (u + 0.044715 * u * u * u)));
        }
        const m = this.affine(f, w[`${l}.w_pr`], w[`${l}.b_pr`], C);
        for (let i = 0; i < C; i++) x[i] += m[i];
      }
      const hf = this.norm(x, w.lnf_g, w.lnf_b), logits = new Float32Array(this.V);
      for (let v = 0; v < this.V; v++) {
        let d = 0;
        for (let i = 0; i < C; i++) d += hf[i] * w.wte[v * C + i];
        logits[v] = d;
      }
      this.pos++;
      return logits;
    }

    // Read a whole window from scratch (used at the start, and when a line gets longer than the brain can hold).
    read(ids) {
      this.reset();
      let logits = null;
      for (const id of ids.slice(-this.T)) logits = this.step(id);
      return logits;
    }

    pick(logits, temperature, topK, random) {
      const order = [...logits.keys()].sort((a, b) => logits[b] - logits[a]).slice(0, topK);
      if (topK === 1) return order[0];
      const top = logits[order[0]] / temperature;
      const ws = order.map(i => Math.exp(logits[i] / temperature - top));
      let r = random() * ws.reduce((a, b) => a + b, 0);
      for (let i = 0; i < order.length; i++) { r -= ws[i]; if (r <= 0) return order[i]; }
      return order[order.length - 1];
    }

    // One line from the cat, optionally about a topic.
    // you: what someone typed to it in its notebook (it answers that). topic: what to talk about, and the word it gets spelling help with.
    // start: words the line must begin with, like "i wish" for its wish list.
    // spell: write only real words (on when the brain carries its word list).
    say({ you = null, topic = null, start = "", copy = true, copyFrom = 0, temperature = 0.8, topK = 12, random = Math.random, maxLetters = 110, spell = true } = {}) {
      start = start.toLowerCase().trim();
      const extra = [...new Set([topic, you, start].filter(Boolean).join(" ").toLowerCase().match(/[a-z']+/g) || [])];
      spell = spell && this.words.size > 0;
      const head = you ? `you: ${you.toLowerCase()}\n` : topic ? `topic: ${topic.toLowerCase()}\n` : "";
      const prompt = head + "cat:" + (start ? " " + start : "");
      const ids = [...prompt].filter(c => this.lut.has(c)).map(c => this.lut.get(c));
      let logits = this.read(ids), out = start;
      topic = topic ? topic.toLowerCase() : null;
      let started = false;   // set once the cat has been helped to start its topic, so it can finish it
      for (let n = 0; n < maxLetters; n++) {
        let pool = logits;
        if (spell) {
          const ok = this.allowed(out, extra);
          if (ok.some(Boolean)) { pool = Float32Array.from(logits); ok.forEach((y, i) => { if (!y) pool[i] = -Infinity; }); }
        }
        let next = this.pick(pool, temperature, topK, random);
        let forced = copy ? copyNext(out, topic, started ? 1 : Math.max(copyFrom, 1), started) : null;
        if (copy && copyFrom === 0 && forced === null && topic && !out.includes(topic)) {
          // Start the topic where a topic usually goes, if its first letter is one the cat was already considering:
          // right after "the", "my" or "a" for "the zumba class", at the start of a sentence for a bare word like "glimbo".
          const lead = ["the ", "my ", "a ", "an "].find(w => topic.startsWith(w)) || "";
          const at = lead ? out.endsWith(lead) && (out.length === lead.length || !/[a-z]/.test(out[out.length - lead.length - 1]))
                          : out.trim() === "" || /[.?!] $/.test(out);
          if (at) {
            const c = this.lut.get(topic[lead.length]);
            const order = [...logits.keys()].sort((a, b) => logits[b] - logits[a]).slice(0, topK);
            if (c !== undefined && order.includes(c)) { forced = topic[lead.length]; started = true; }
          }
        }
        if (forced === END) {
          if (/[a-z0-9'-]/.test(this.vocab[next])) {
            let best = -1;
            for (let i = 0; i < this.V; i++) {
              const c = this.vocab[i];
              if (/[a-z0-9'-]/.test(c) || (c === "\n" && out.length < 30)) continue;   // and not end the line on a bare topic
              if (best < 0 || logits[i] > logits[best]) best = i;
            }
            next = best;
          }
        } else if (forced !== null && this.lut.has(forced)) next = this.lut.get(forced);
        if (this.vocab[next] === "\n") break;
        out += this.vocab[next];
        ids.push(next);
        logits = ids.length > this.T ? this.read(ids) : this.step(next);
      }
      return out.trim();
    }
  }

  if (typeof module !== "undefined") module.exports = TinyCat;
  else root.TinyCat = TinyCat;
})(typeof window !== "undefined" ? window : globalThis);
