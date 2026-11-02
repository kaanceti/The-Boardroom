"""Blind test, round 3, step 2: a separate Claude (Opus) compares the two answers to each question.

The same judge as rounds 1 and 2: the instructions, the neutral labels and the scoring are taken word for word
from ../judge.py. Each pair is judged twice with the order swapped, and a win only counts when both orders agree.
Exit code 0: every judgement done (the totals are printed and saved in summary.json). Exit code 2: run it again later.
"""
import importlib.util, json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
import boardroom as br

_argv, sys.argv = sys.argv, sys.argv[:1]   # the round 1 judge reads its own arguments when it loads
_spec = importlib.util.spec_from_file_location("round1_judge", HERE.parent / "judge.py")
round1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(round1)
sys.argv = _argv

JUDGE_MODEL = "opus"
ANSWERS = json.loads((HERE / "answers.json").read_text(encoding="utf-8"))
OUT = HERE / "judgments.json"
CRITERIA = round1.CRITERIA


def judge(key: str, board_first: bool):
    q = ANSWERS[key]
    board, single = round1.neutral(q["board"]["text"]), q["single"]["text"]
    a, b = (board, single) if board_first else (single, board)
    prompt = f"Question:\n{q['question']}\n\n=== Answer A ===\n{a}\n\n=== Answer B ===\n{b}\n\nReturn the JSON now."
    for _ in range(3):
        res = br.ask_claude(round1.SYSTEM, prompt, [], JUDGE_MODEL)
        d = round1.parse(res.get("text", "")) if res.get("ok") else None
        if d:
            board_side, single_side = ("A", "B") if board_first else ("B", "A")
            winner = {"tie": "tie", board_side: "board", single_side: "single"}[d["winner"]]
            return {"board": d[board_side], "single": d[single_side], "winner": winner,
                    "reason": d.get("reason", ""), "seconds": res.get("seconds")}
        print(f"   retry {key} board_first={board_first}: {(res.get('error') or res.get('text') or '')[:120]}", flush=True)
        if round1.limited(res.get("error") or ""):
            return None
        time.sleep(5)
    return None


def summary(results: dict) -> dict:
    wins = {"board": 0, "tie": 0, "single": 0}
    scores = {side: {c: [] for c in CRITERIA} for side in ("board", "single")}
    for k in ANSWERS:
        a, b = results[f"{k}:board_first"], results[f"{k}:single_first"]
        wins[a["winner"] if a["winner"] == b["winner"] else "tie"] += 1
        for side in scores:
            for c in CRITERIA:
                scores[side][c] += [a[side][c], b[side][c]]
    avg = {side: {c: round(sum(v) / len(v), 1) for c, v in s.items()} for side, s in scores.items()}
    return {"wins": wins, "average": avg, "judge": JUDGE_MODEL, "questions": len(ANSWERS)}


def main() -> int:
    missing = [k for k, q in ANSWERS.items() if not (q.get("board", {}).get("ok") and q.get("single", {}).get("ok"))]
    if missing or len(ANSWERS) < 15:
        print("Answer every question first (run.py).", flush=True)
        return 2
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
    if any(f"{k}:{o}" not in results for k in ANSWERS for o in ("board_first", "single_first")):
        print("Some judgements are missing (usage limit?). Run it again later to finish.", flush=True)
        return 2
    s = summary(results)
    (HERE / "summary.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
    print(f"\nBoard {s['wins']['board']}, tie {s['wins']['tie']}, Opus on its own {s['wins']['single']}", flush=True)
    for c in CRITERIA:
        print(f"   {c:<10} board {s['average']['board'][c]:.1f}   Opus {s['average']['single'][c]:.1f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
