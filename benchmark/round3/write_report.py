"""Write RESULTS.md for round 3: the totals, every question, both answers, the scores and the judge's reasons."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = json.loads((HERE / "answers.json").read_text(encoding="utf-8"))
J = json.loads((HERE / "judgments.json").read_text(encoding="utf-8"))
S = json.loads((HERE / "summary.json").read_text(encoding="utf-8"))
C = ("usefulness", "accuracy", "risk", "clarity")
NAMES = {"usefulness": "Usefulness", "accuracy": "Accuracy", "risk": "Risk spotting", "clarity": "Clarity"}
WIN = {"board": "Board", "single": "Opus alone", "tie": "Tie"}
KEYS = sorted(A, key=int)


def result(k):
    a, b = J[f"{k}:board_first"], J[f"{k}:single_first"]
    winner = a["winner"] if a["winner"] == b["winner"] else "tie"
    board = {c: (a["board"][c] + b["board"][c]) / 2 for c in C}
    single = {c: (a["single"][c] + b["single"][c]) / 2 for c in C}
    return winner, board, single, a, b


def words(text):
    return len(re.findall(r"\S+", text))


def demote(text):
    return re.sub(r"^(#{1,3}) ", lambda m: "#" * (len(m.group(1)) + 2) + " ", text.strip(), flags=re.M)


def details(summary, body):
    return f"<details>\n<summary>{summary}</summary>\n\n{demote(body)}\n\n</details>\n"


def short(q, n=70):
    return q if len(q) <= n else q[:n].rsplit(" ", 1)[0] + "…"


rows = [result(k) for k in KEYS]
w = S["wins"]
split = [k for k, r in zip(KEYS, rows) if r[0] == "tie"]
second = sum(1 for k in split if J[f"{k}:board_first"]["winner"] == "single" and J[f"{k}:single_first"]["winner"] == "board")
avg = lambda xs: sum(xs) / len(xs)
board_words, single_words = avg([words(A[k]["board"]["text"]) for k in KEYS]), avg([words(A[k]["single"]["text"]) for k in KEYS])
board_secs, single_secs = avg([A[k]["board"]["seconds"] for k in KEYS]), avg([A[k]["single"]["seconds"] for k in KEYS])
board_calls = avg([A[k]["board"]["calls"] for k in KEYS])
setups = {json.dumps(A[k]["setup"], sort_keys=True) for k in KEYS}

out = ["# Round 3 results: today's board against Claude Opus on its own", "",
       "The [plan](PLAN.md) was written before any answer existed. Fifteen new questions, each answered by a full "
       "Boardroom meeting and by one Claude Opus call with the same web tools, then judged blind by Claude Opus, twice "
       "per question with the order swapped. A win only counts when both orders agree.", "",
       f"**Board {w['board']}, tie {w['tie']}, Opus alone {w['single']}.**", "",
       "| Average score out of 10 | Board | Opus alone |", "| --- | --- | --- |"]
for c in C:
    b, s = S["average"]["board"][c], S["average"]["single"][c]
    out.append(f"| {NAMES[c]} | {'**%.1f**' % b if b > s else '%.1f' % b} | {'**%.1f**' % s if s > b else '%.1f' % s} |")
out += ["",
        f"- **The ties.** In {'all ' + str(len(split)) if second == len(split) else f'{second} of the {len(split)}'} ties the "
        "judge picked whichever answer it read second, both times. That is a judge leaning on order, not a loss for either side, and it is why every pair is judged twice.",
        f"- **Cost.** A board answer took {board_calls:.0f} Claude calls and {board_secs:.0f} seconds on average; "
        f"Opus alone took 1 call and {single_secs:.0f} seconds.",
        f"- **Length.** Board answers averaged {board_words:.0f} words, Opus alone {single_words:.0f}. Both ran over "
        "the 500-word limit they were given. AI judges can favour longer answers.",
        "- **Where the board lost points.** Clarity, and in questions 2 and 8 (both ties) the judge marked it down for "
        "survey figures it could not verify. Both came from the Scout's web research and the Chair kept them.",
        "- **The app did not change during the test.** Every answer carries the same fingerprint: "
        + ", ".join(f"{f} `{v}`" for f, v in json.loads(setups.pop()).items()) + (" (and others)" if setups else "") + ".",
        "- **Blind reviews.** No reviewer was shown a name. One of the 60 reviews guessed a member from their style "
        "(\"Operator-style caution\"). In the first attempt, before the fix, 22 of the first 32 reviews named who wrote what.",
        "- **Complete meetings only.** Meetings stopped by the Claude plan's session limit were run again later, so "
        "every answer here comes from a full meeting.", "",
        "Limits stated before the test: the judge is the same model as Opus alone and as the Chair, fifteen questions "
        "is a small sample, and each question was run once.", "",
        "## Every question", "",
        "| # | Question | Winner | Judge, board shown first | Judge, Opus shown first | Score (board vs Opus) |",
        "| --- | --- | --- | --- | --- | --- |"]
for k, (win, b, s, x, y) in zip(KEYS, rows):
    out.append(f"| [{k}](#question-{k}) | {short(A[k]['question'])} | {WIN[win]} | {WIN[x['winner']]} | "
               f"{WIN[y['winner']]} | {avg(list(b.values())):.1f} vs {avg(list(s.values())):.1f} |")
out.append("")

for k, (win, b, s, x, y) in zip(KEYS, rows):
    q = A[k]
    out += [f"## Question {k}", "", f"**{q['question']}**", "",
            "| | Board | Opus alone |", "| --- | --- | --- |"]
    out += [f"| {NAMES[c]} | {b[c]:.1f} | {s[c]:.1f} |" for c in C]
    out += [f"| **Winner** | {WIN[win]} | |", "",
            f"Judge, board shown first (A is the board): \"{x['reason']}\"", "",
            f"Judge, Opus shown first (A is Opus alone): \"{y['reason']}\"", "",
            details(f"Board answer ({words(q['board']['text'])} words)", q["board"]["text"]),
            details(f"Opus alone ({words(q['single']['text'])} words)", q["single"]["text"]),
            f"Full meeting: [statements and cross-examination](meetings/{q['board']['meeting_id']}.md)", ""]

(HERE / "RESULTS.md").write_text("\n".join(out), encoding="utf-8")
print("wrote RESULTS.md")
