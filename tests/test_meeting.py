"""A whole board meeting, run against a fake `claude` command (tests/fake_claude.py), so it costs nothing."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import boardroom as br  # noqa: E402

DEFAULT_NAMES = [m["name"] for m in br.load_board()["members"]]


class MeetingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        fake = Path(__file__).with_name("fake_claude.py")
        if os.name == "nt":
            (bin_dir / "claude.cmd").write_text(f'@"{sys.executable}" "{fake}" %*\n', encoding="utf-8")
        else:
            shim = bin_dir / "claude"
            shim.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{fake}" "$@"\n', encoding="utf-8")
            shim.chmod(0o755)
        self.log = self.tmp / "prompts.jsonl"
        self.saved = {k: getattr(br, k) for k in ("MEETINGS", "FILES", "WORKDIR")}
        self.env = {k: os.environ.get(k) for k in ("PATH", "FAKE_CLAUDE_LOG")}
        os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
        os.environ["FAKE_CLAUDE_LOG"] = str(self.log)
        br.MEETINGS, br.FILES, br.WORKDIR = self.tmp / "meetings", self.tmp / "files", self.tmp / "workdir"
        for folder in (br.MEETINGS, br.FILES, br.WORKDIR):
            folder.mkdir()

    def tearDown(self):
        for k, v in self.saved.items():
            setattr(br, k, v)
        for k, v in self.env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.tmp, ignore_errors=True)

    def prompts(self, kind):
        lines = self.log.read_text(encoding="utf-8").splitlines() if self.log.exists() else []
        return [p["prompt"] for p in map(json.loads, lines) if p["kind"] == kind]

    def run_one(self, **kwargs):
        m = br.new_meeting("Should I open a second café?", "", **kwargs)
        br.run_meeting(m)
        return m

    def test_full_meeting(self):
        m = self.run_one(mode="full")
        self.assertEqual(len(m["statements"]), 4)
        self.assertEqual(len(m["reviews"]), 4)
        self.assertTrue(all(p["ok"] for p in m["statements"] + m["reviews"]))
        self.assertTrue(m["resolution"]["ok"])
        self.assertEqual(m["verdict"]["call"], "partly")
        self.assertNotIn("Your leaning", m["resolution"]["text"])   # the verdict is taken out of the write-up
        minutes = (br.MEETINGS / f"{m['id']}.md").read_text(encoding="utf-8")
        self.assertIn("Should I open a second café?", minutes)
        self.assertIn("Partly agreed with you", minutes)

    def test_each_seat_uses_its_own_model(self):
        m = self.run_one(mode="full")
        board = br.load_board()
        expected = {s["id"]: s["model"] for s in board["members"]}
        self.assertEqual({s["id"]: s["model"] for s in m["statements"]}, expected)
        self.assertEqual(m["resolution"]["model"], board["chair"]["model"])

    def test_reviewers_never_see_names(self):
        self.run_one(mode="full")
        reviews = self.prompts("review")
        self.assertEqual(len(reviews), 4)
        for prompt in reviews:
            for name in DEFAULT_NAMES:
                self.assertNotIn(name, prompt)
            self.assertEqual(prompt.count("\nStatement "), 3)   # the three others, by letter only
            self.assertIn("As [member], I think it works.", prompt)

    def test_reviewers_never_see_the_owners_names_either(self):
        self.run_one(mode="full", names={"skeptic": "Bob", "scout": "Penny"})
        for prompt in self.prompts("review"):
            for name in DEFAULT_NAMES + ["Bob", "Penny"]:
                self.assertNotIn(name, prompt)

    def test_quick_meeting_skips_the_cross_examination(self):
        m = self.run_one(mode="quick")
        self.assertEqual(len(m["statements"]), 4)
        self.assertEqual(m["reviews"], [])
        self.assertTrue(m["resolution"]["ok"])

    def test_punishment_corner(self):
        m = self.run_one(mode="full", absent=["advocate"])
        self.assertEqual([s["id"] for s in m["statements"]], ["skeptic", "operator", "scout"])
        self.assertEqual(len(m["reviews"]), 3)
        self.assertIn("punishment corner", (br.MEETINGS / f"{m['id']}.md").read_text(encoding="utf-8"))


class HideNamesTest(unittest.TestCase):
    names = ["Skeptic", "Advocate", "Operator", "Scout"]

    def test_signature_line_is_dropped(self):
        self.assertEqual(br.hide_names("**Skeptic's statement**\n\nIt will fail.", self.names), "It will fail.")
        self.assertEqual(br.hide_names("**Statement from Scout (evidence)**\nFacts.", self.names), "Facts.")

    def test_other_mentions_become_member(self):
        self.assertEqual(br.hide_names("As the Operator, I want dates.", self.names), "As [member], I want dates.")

    def test_sentences_are_kept(self):
        text = "**The usual answer: keep it.** I argue sell."
        self.assertEqual(br.hide_names(text, self.names), text)

    def test_ordinary_words_are_left_alone(self):
        text = "First scout the market, then advocate for a trial."
        self.assertEqual(br.hide_names(text, self.names), text)


if __name__ == "__main__":
    unittest.main()
