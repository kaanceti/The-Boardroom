"""The office cat's tiny language model: its maths, the browser copy, its spelling and its safety filter."""
import json
import re
import shutil
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "cat"
sys.path.insert(0, str(CAT))
import tinycat  # noqa: E402
import safety  # noqa: E402

PROMPTS = [("good kitty", None), ("what do you think of the bake sale?", "the bake sale"), ("hiya kibi", None),
           ("how was glimbo?", "glimbo"), ("tell me about my nephew's football match", "my nephew's football match")]


def starter():
    """The starter brain as the browser sees it: the app ships its numbers rounded to half precision."""
    p, cfg, vocab, _ = tinycat.load(CAT / "starter-brain.npz")
    p = {k: v.astype(np.float16).astype(np.float32) for k, v in p.items()}
    return p, cfg, vocab, tinycat.load_words(CAT / "starter-brain.npz")


class GradientTest(unittest.TestCase):
    def test_backpropagation_matches_a_slow_numerical_check(self):
        """The hand-written backward pass against nudging each number and watching the loss."""
        cfg = dict(context=8, width=8, layers=2, heads=2)
        p = {k: v.astype(np.float64) for k, v in tinycat.init(7, **cfg, seed=1).items()}
        rng = np.random.default_rng(0)
        idx, targets = rng.integers(0, 7, (2, 6)), rng.integers(0, 7, (2, 6))
        _, cache = tinycat.forward(p, idx, cfg, targets)
        grads = tinycat.backward(p, cache, cfg)
        eps = 1e-5
        for name in ("wte", "wpe", "0.w_qkv", "0.ln1_g", "1.w_fc", "1.b_pr", "lnf_b"):
            flat = p[name].reshape(-1)
            for i in rng.choice(flat.size, 4, replace=False):
                old = flat[i]
                flat[i] = old + eps
                up = tinycat.forward(p, idx, cfg, targets)[0]
                flat[i] = old - eps
                down = tinycat.forward(p, idx, cfg, targets)[0]
                flat[i] = old
                numeric = (up - down) / (2 * eps)
                self.assertAlmostEqual(grads[name].reshape(-1)[i], numeric, delta=1e-6 + 1e-3 * abs(numeric),
                                       msg=f"{name}[{i}]")


class StarterBrainTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p, cls.cfg, cls.vocab, cls.words = starter()

    @unittest.skipUnless(shutil.which("node"), "needs Node.js")
    def test_browser_and_python_write_the_same_lines(self):
        """cat/tinycat.js (the browser) and cat/tinycat.py must be the same model, letter for letter."""
        script = ("const fs = require('fs'); const TinyCat = require(process.argv[1]);"
                  "const cat = new TinyCat(JSON.parse(fs.readFileSync(process.argv[2], 'utf8')));"
                  "for (const [you, topic] of JSON.parse(process.argv[3])) for (const spell of [true, false])"
                  "  console.log(cat.say({ you, topic, topK: 1, copyFrom: 0, spell }));")
        out = subprocess.run(["node", "-e", script, str(CAT / "tinycat.js"), str(CAT / "starter-brain.json"),
                              json.dumps(PROMPTS)], capture_output=True, text=True, encoding="utf-8", check=True)
        rng = np.random.default_rng(0)
        python = [tinycat.say(self.p, self.cfg, self.vocab, rng, topic=topic, you=you, top_k=1, copy_from=0, words=w)[0]
                  for you, topic in PROMPTS for w in (self.words, None)]
        self.assertEqual(out.stdout.splitlines(), python)

    def test_it_only_writes_real_words(self):
        rng = np.random.default_rng(7)
        known = set(self.words)
        total = unknown = 0
        for you, topic in PROMPTS * 4:
            line = tinycat.say(self.p, self.cfg, self.vocab, rng, topic=topic, you=you, words=self.words)[0]
            allowed = known | set(re.findall(r"[a-z']+", f"{you} {topic or ''}"))
            # The last word can be cut off when a line reaches its letter limit, so it is left out.
            for word in re.findall(r"[a-z']+", line)[:-1]:
                total += 1
                unknown += word.strip("'") not in allowed and word not in allowed
        self.assertGreater(total, 100)
        self.assertLessEqual(unknown / total, 0.01)

    def test_it_uses_the_topic_it_is_given(self):
        rng = np.random.default_rng(3)
        for topic in ("the bake sale", "the zumba class", "glimbo"):
            lines = tinycat.say(self.p, self.cfg, self.vocab, rng, topic=topic, you=f"what do you think of {topic}?",
                                n=5, words=self.words)
            self.assertGreaterEqual(sum(topic in line for line in lines), 4, lines)


class SafetyTest(unittest.TestCase):
    def test_advice_violence_and_swearing_are_left_out(self):
        for line in ("you should sue your landlord", "ask a doctor about the dose", "what the fuck", "i will murder the pen"):
            self.assertFalse(safety.safe(line), line)

    def test_ordinary_cat_talk_is_kept(self):
        for line in ("i sat on your notes. that was the help.", "the budget smells like coffee", "the class was classy"):
            self.assertTrue(safety.safe(line), line)

    def test_unsafe_meeting_text_never_reaches_its_lessons(self):
        """A meeting full of advice and swearing: none of it may end up in what the cat practises on."""
        import prepare
        with tempfile.TemporaryDirectory() as tmp:
            meeting = Path(tmp) / "m.json"
            meeting.write_text(json.dumps({
                "stage": "done", "agenda": "Should I sue my landlord?", "names": {},
                "statements": [{"ok": True, "text": "You should sue them. What the fuck is that clause. I recommend a lawyer."}],
                "resolution": {"ok": True, "text": "The landlord dispute is a real worry. Ask a doctor about the dose."}}),
                encoding="utf-8")
            lessons, _ = prepare.build([meeting])
        text = "\n".join(lessons).lower()
        for phrase in ("sue", "fuck", "lawyer", "doctor", "dose", "i recommend"):
            self.assertIsNone(re.search(rf"\b{phrase}\b", text), f"'{phrase}' got into its lessons")
        self.assertIn("landlord", text)   # the safe part of the meeting is still learned


if __name__ == "__main__":
    unittest.main()
