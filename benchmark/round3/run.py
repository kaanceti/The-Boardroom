"""Blind test, round 3, step 1: today's board against Claude Opus on its own, on 15 new questions.

The board runs exactly as the app does: members.json as it is, a full meeting. The single answer is one Opus call
with the same web tools, the same owner location and the same answer format as rounds 1 and 2 (taken from ../run.py).
Results are saved after every question, so the run can stop and resume.
Exit code 0: every question answered. Exit code 2: stopped early (usage limit or a failed answer); run it again later.
"""
import hashlib, importlib.util, json, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
import boardroom as br

# The test meetings stay in this folder, not in your Past meetings, and the cat does not learn from them.
br.MEETINGS = HERE / "meetings"
br.FILES = ROOT / "data" / "benchmark-work"
br.MEETINGS.mkdir(exist_ok=True)
br.FILES.mkdir(parents=True, exist_ok=True)
br.CAT_AUTO["on"] = False

# The single answer's instructions and format, word for word from rounds 1 and 2.
_spec = importlib.util.spec_from_file_location("round1_run", HERE.parent / "run.py")
round1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(round1)

SINGLE_MODEL = "opus"
QUESTIONS = json.loads((HERE / "questions.json").read_text(encoding="utf-8"))
OUT = HERE / "answers.json"


def fingerprint() -> dict:
    """Which version of the board answered, so a change to the app mid-test would show."""
    return {f: hashlib.md5((ROOT / f).read_bytes()).hexdigest()[:12] for f in ("boardroom.py", "members.json")}


def done(entry: dict) -> bool:
    return bool(entry.get("board", {}).get("ok") and entry.get("single", {}).get("ok"))


def main() -> int:
    board = br.load_board()
    system = round1.BASE_SYSTEM + br.where(board)
    results = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for i, q in enumerate(QUESTIONS, 1):
        key = str(i)
        if done(results.get(key, {})):
            continue
        print(f"[{time.strftime('%H:%M:%S')}] Question {i} of {len(QUESTIONS)}: {q[:60]}", flush=True)
        entry = results.get(key, {"question": q})
        if not entry.get("single", {}).get("ok"):
            res = br.ask_claude(system, f"Question from the owner:\n{q}\n\n{round1.BASE_FORMAT}", ["WebSearch", "WebFetch"], SINGLE_MODEL)
            entry["single"] = {**res, "model": SINGLE_MODEL}
            print(f"   Opus on its own: {'done' if res['ok'] else 'failed'} ({res.get('seconds')}s)", flush=True)
        if not entry.get("board", {}).get("ok"):
            m = br.new_meeting(q, "", "full")
            started = time.time()
            br.run_meeting(m)
            res = m.get("resolution") or {}
            # Only a complete meeting counts: if a member dropped out (a usage limit, say), the meeting is run again.
            parts = m["statements"] + (m.get("reviews") or [])
            seats = len(board["members"])
            full = len(m["statements"]) == seats and len(m.get("reviews") or []) == seats and all(p.get("ok") for p in parts)
            problems = "; ".join((p.get("error") or "failed")[:150] for p in parts if not p.get("ok"))
            entry["board"] = {"ok": bool(res.get("ok")) and full, "text": res.get("text", ""),
                              "error": res.get("error") or problems or (None if full else "the meeting was not complete"),
                              "meeting_id": m["id"], "seconds": round(time.time() - started, 1),
                              "calls": len(m["statements"]) + len(m.get("reviews") or []) + 1,
                              "models": {**{s["id"]: s.get("model") for s in m["statements"]}, "chair": res.get("model")},
                              "verdict": m.get("verdict")}
            print(f"   board: {'done' if entry['board']['ok'] else 'failed'} ({entry['board']['seconds']}s)", flush=True)
        entry["setup"] = fingerprint()
        results[key] = entry
        OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        errors = [entry.get("single", {}).get("error") or "", entry.get("board", {}).get("error") or ""]
        if any(round1.limited(e) for e in errors):
            print("Your Claude plan reached its usage limit. Stopping here; run it again later to carry on.", flush=True)
            return 2
    left = [k for k in map(str, range(1, len(QUESTIONS) + 1)) if not done(results.get(k, {}))]
    if left:
        print(f"{len(left)} question(s) still need an answer: {', '.join(left)}. Run it again to retry them.", flush=True)
        return 2
    print("All questions answered.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
