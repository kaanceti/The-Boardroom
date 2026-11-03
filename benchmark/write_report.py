"""Write all-answers.md: every question, both answers, the scores and the judge's reasons, for GitHub."""
import json, re, statistics as st
from pathlib import Path
HERE = Path(__file__).resolve().parent
A = json.loads((HERE / "answers.json").read_text(encoding="utf-8"))
V2 = json.loads((HERE / "answers_v2.json").read_text(encoding="utf-8"))
J1 = json.loads((HERE / "judgments.json").read_text(encoding="utf-8"))
J2 = json.loads((HERE / "judgments_answers_v2.json").read_text(encoding="utf-8"))
C = ("usefulness", "accuracy", "risk", "clarity")
NAMES = {"usefulness": "Usefulness", "accuracy": "Accuracy", "risk": "Risk spotting", "clarity": "Clarity"}
WIN = {"board": "Board", "single": "Single", "tie": "Tie"}

def result(J, k):
    a, b = J[f"{k}:board_first"], J[f"{k}:single_first"]
    winner = a["winner"] if a["winner"] == b["winner"] else "tie"
    board = {c: (a["board"][c] + b["board"][c]) / 2 for c in C}
    single = {c: (a["single"][c] + b["single"][c]) / 2 for c in C}
    return winner, board, single, a["reason"], b["reason"]

def demote(text):
    # answers use ## headings; nest them under this page's headings
    return re.sub(r"^(#{1,3}) ", lambda m: "#" * (len(m.group(1)) + 2) + " ", text.strip(), flags=re.M)

def avg(d):
    return sum(d.values()) / len(d)

def details(summary, body):
    return f"<details>\n<summary>{summary}</summary>\n\n{demote(body)}\n\n</details>\n"

out = ["# Blind test: every question and answer", "",
       "Fifteen questions, each answered by a single Claude call and by a full Boardroom meeting, then judged blind "
       "by Claude Opus. Method and summary: [benchmark/README.md](README.md) and the main [README](../README.md#how-it-got-here).", "",
       "- **Round 1** judged the board's original resolution. **Round 2** re-ran only the Chair on the same meetings "
       "with the reworked write-up; the members' statements and the single answers are identical in both rounds.",
       "- Scores are out of 10, averaged over two judgements with the order swapped. A win only counts when both orders agree.",
       "- Member names were replaced with neutral labels (\"Analyst 1\" and so on) before judging; the answers below "
       "are shown as the board wrote them. Full meeting minutes are in [meetings/](meetings/).", "",
       "## Which is which", "",
       "| Label | What it means |",
       "| --- | --- |",
       "| **Board** | The Boardroom: four members give statements and cross-examine each other, then the Chair writes the answer (9 Claude calls). |",
       "| **Single** | One Claude call with the same model and web tools, asked for a decision, risks, criticism and next steps. |",
       "| **Round 1** | The board's answer as the Chair first wrote it (it narrated where the members agreed and disagreed). |",
       "| **Round 2** | The Chair re-run on the same meetings with the reworked write-up. The single answers did not change. |",
       "| **A and B** | The judge saw two unnamed answers. In every judge quote on this page, **A is the Board and B is the Single answer**. |",
       "| **Analyst 1 to 4** | How the judge saw the members: 1 Skeptic, 2 Advocate, 3 Operator, 4 Scout. |",
       "| **Personalities** | Skeptic: Melancholic. Advocate: Sanguine. Operator: Choleric. Scout: Phlegmatic. Chair: Balanced. This test used the milder versions; the Skeptic and Advocate have since been made extreme. |",
       "",
       "## Summary", "",
       "| # | Question | Round 1 | Round 2 | Round 2 score (board vs single) |",
       "| --- | --- | --- | --- | --- |"]
for k, q in A.items():
    w1 = result(J1, k)[0]; w2, b2, s2, _, _ = result(J2, k)
    short = q["question"] if len(q["question"]) <= 70 else q["question"][:70].rsplit(" ", 1)[0] + "…"
    out.append(f"| [{k}](#question-{k}) | {short} | {WIN[w1]} | {WIN[w2]} | {avg(b2):.1f} vs {avg(s2):.1f} |")
r1 = [result(J1, k) for k in A]; r2 = [result(J2, k) for k in A]
count = lambda rs, w: sum(1 for r in rs if r[0] == w)
out += ["", f"**Totals.** Round 1: board {count(r1,'board')}, tie {count(r1,'tie')}, single {count(r1,'single')}. "
        f"Round 2: board {count(r2,'board')}, tie {count(r2,'tie')}, single {count(r2,'single')}.", ""]

for k, q in A.items():
    w1, b1, s1, _, _ = result(J1, k)
    w2, b2, s2, reason_r2, _ = result(J2, k)
    reason_r1 = J1[f"{k}:board_first"]["reason"]
    mid = q["board"]["meeting_id"]
    out += [f"## Question {k}", "", f"**{q['question']}**", "",
            "| | Round 1 board | Round 1 single | Round 2 board | Round 2 single |",
            "| --- | --- | --- | --- | --- |"]
    for c in C:
        out.append(f"| {NAMES[c]} | {b1[c]:.1f} | {s1[c]:.1f} | {b2[c]:.1f} | {s2[c]:.1f} |")
    out += [f"| **Winner** | {WIN[w1]} | | {WIN[w2]} | |", "",
            f"Judge, round 2 (A = Board, B = Single): \"{reason_r2}\"", "",
            f"Judge, round 1 (A = Board, B = Single): \"{reason_r1}\"", "",
            details("Board answer, round 2 (reworked Chair)", V2[k]["text"]),
            details("Single Claude answer", q["single"]["text"]),
            details("Board answer, round 1 (original Chair)", q["board"]["text"]),
            f"Full meeting: [statements and cross-examination](meetings/{mid}.md)", ""]

(HERE / "all-answers.md").write_text("\n".join(out), encoding="utf-8")
print("wrote all-answers.md", sum(len(x) for x in out), "chars")
