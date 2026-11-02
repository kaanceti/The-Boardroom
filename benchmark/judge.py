"""Blind test, step 2: a separate Claude (Opus) compares the two answers to each question.

Each pair is judged twice with the order swapped, and a win only counts when both orders agree.
The board's own labels (member names, "the board") are replaced with neutral words first, so the
judge is not told which answer came from the board. The board's answer still has its own headings,
so the test is blind to the labels, not to the format.
"""
import json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "app"))
import boardroom as br

ANSWERS = json.loads((HERE / "answers.json").read_text(encoding="utf-8"))
JUDGE_MODEL = sys.argv[1] if len(sys.argv) > 1 else "opus"
# Optional: judge a second version of the board's answers (round 2) against the same single answers.
BOARD_FILE = sys.argv[2] if len(sys.argv) > 2 else None
BOARD_V2 = json.loads((HERE / BOARD_FILE).read_text(encoding="utf-8")) if BOARD_FILE else None
OUT = HERE / ("judgments.json" if not BOARD_FILE else f"judgments_{Path(BOARD_FILE).stem}.json")
CRITERIA = ("usefulness", "accuracy", "risk", "clarity")

SYSTEM = (
    "You are an expert, strict evaluator of advice written for one person. You will see their question and two answers, A and B. "
    "Score each answer from 1 to 10 on:\n"
    "- usefulness: would it actually help this person decide and act?\n"
    "- accuracy: are the claims correct, is uncertainty flagged, and is nothing invented?\n"
    "- risk: does it spot the risks that matter, including legal, ethical and money risks?\n"
    "- clarity: is it easy to follow and free of padding?\n"
    "Then choose the overall winner: A, B or tie. A longer answer is not better by default, and format only matters "
    "where it changes usefulness or clarity. Ignore any hint about how an answer was produced. An answer may refer to "
    "analysts whose notes the person can also read, so do not mark it down for mentioning them.\n"
    'Reply with JSON only, no other text: {"A": {"usefulness": n, "accuracy": n, "risk": n, "clarity": n}, '
    '"B": {"usefulness": n, "accuracy": n, "risk": n, "clarity": n}, "winner": "A" or "B" or "tie", "reason": "one sentence"}'
)

def neutral(text: str) -> str:
    t = (text.replace("## Where the board agreed", "## Common ground")
             .replace("## Where the board disagreed", "## Points of disagreement")
             .replace("## Where I overrule the board", "## Arguments I reject")
             .replace("## Board notes", "## Analyst notes"))
    for i, name in enumerate(("Skeptic", "Advocate", "Operator", "Scout"), 1):
        t = re.sub(rf"\b{name}\b", f"Analyst {i}", t)
    t = re.sub(r"\bThe board\b", "The analysts", t)
    t = re.sub(r"\bthe board\b", "the analysts", t)
    t = re.sub(r"\bboard\b", "analysts", t)
    t = re.sub(r"\bmembers?\b", "analysts", t)
    return t

def parse(text: str):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
        for side in "AB":
            d[side] = {c: float(d[side][c]) for c in CRITERIA}
        d["winner"] = str(d.get("winner", "tie")).strip().upper().replace("TIE", "tie")
        if d["winner"] not in ("A", "B", "tie"):
            return None
        return d
    except (ValueError, KeyError, TypeError):
        return None

def judge(key: str, board_first: bool):
    q = ANSWERS[key]
    board_text = BOARD_V2[key]["text"] if BOARD_V2 else q["board"]["text"]
    board, single = neutral(board_text), q["single"]["text"]
    a, b = (board, single) if board_first else (single, board)
    prompt = f"Question:\n{q['question']}\n\n=== Answer A ===\n{a}\n\n=== Answer B ===\n{b}\n\nReturn the JSON now."
    for attempt in range(3):
        res = br.ask_claude(SYSTEM, prompt, [], JUDGE_MODEL)
        d = parse(res.get("text", "")) if res.get("ok") else None
        if d:
            board_side, single_side = ("A", "B") if board_first else ("B", "A")
            winner = {"tie": "tie", board_side: "board", single_side: "single"}[d["winner"]]
            return {"board": d[board_side], "single": d[single_side], "winner": winner,
                    "reason": d.get("reason", ""), "seconds": res.get("seconds")}
        print(f"   retry {key} board_first={board_first}: {(res.get('error') or res.get('text') or '')[:120]}", flush=True)
        time.sleep(5)
    return None

def main():
    results = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    jobs = [(k, bf) for k in ANSWERS for bf in (True, False) if f"{k}:{'board_first' if bf else 'single_first'}" not in results]
    print(f"{len(jobs)} judgements to run with {JUDGE_MODEL}", flush=True)
    with ThreadPoolExecutor(3) as pool:
        for (k, bf), r in zip(jobs, pool.map(lambda j: judge(*j), jobs)):
            name = f"{k}:{'board_first' if bf else 'single_first'}"
            print(f"[{time.strftime('%H:%M:%S')}] {name}: {r and r['winner']}", flush=True)
            if r:
                results[name] = r
                OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Done.", flush=True)

if __name__ == "__main__":
    main()
