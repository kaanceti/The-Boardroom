"""Blind test, step 1: answer each question with a full Boardroom meeting and with a single Claude call.

Same model, same tools and the same answer format, so the only difference is the board's process.
Results are saved after every question, so the run can stop and resume.
"""
import json, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "app"))
import boardroom as br

OUT = HERE / "answers.json"
QUESTIONS = json.loads((HERE / "questions.json").read_text(encoding="utf-8"))
MODEL = br.load_board().get("model", "sonnet")

BASE_SYSTEM = ("You are an honest advisor to one person (the owner). Give a clear recommendation and honest criticism. "
               "Never flatter the owner and never invent facts; say what you are unsure of.")
BASE_FORMAT = (
    "Answer using these headings:\n## Decision\nOne clear recommendation in two or three sentences.\n"
    "## Main risks\n## Honest criticism for the owner\nWhat the owner is getting wrong or not seeing.\n"
    "## Next steps\nUp to three concrete actions.\n\n"
    + br.RULES.format(words=500)
)

def limited(text: str) -> bool:
    t = (text or "").lower()
    return "limit" in t and ("usage" in t or "rate" in t or "reached" in t or "hit your" in t)

def main():
    results = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for i, q in enumerate(QUESTIONS, 1):
        key = str(i)
        if key in results and results[key].get("board", {}).get("ok") and results[key].get("single", {}).get("ok"):
            continue
        print(f"[{time.strftime('%H:%M:%S')}] Q{i}: {q[:60]}", flush=True)
        entry = results.get(key, {"question": q})
        if not entry.get("single", {}).get("ok"):
            entry["single"] = br.ask_claude(BASE_SYSTEM, f"Question from the owner:\n{q}\n\n{BASE_FORMAT}", ["WebSearch", "WebFetch"], MODEL)
            print(f"   single: ok={entry['single']['ok']} {entry['single'].get('seconds')}s", flush=True)
        if not entry.get("board", {}).get("ok"):
            m = br.new_meeting(q, "", "full")
            started = time.time()
            br.run_meeting(m)
            res = m.get("resolution") or {}
            entry["board"] = {"ok": bool(res.get("ok")), "text": res.get("text", ""), "error": res.get("error"),
                              "meeting_id": m["id"], "seconds": round(time.time() - started, 1),
                              "calls": len(m["statements"]) + len(m.get("reviews") or []) + 1}
            print(f"   board: ok={entry['board']['ok']} {entry['board']['seconds']}s", flush=True)
        results[key] = entry
        OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        errs = [entry.get("single", {}).get("error") or "", entry.get("board", {}).get("error") or ""]
        if any(limited(e) for e in errs):
            print("Usage limit reached. Stopping; run again later to resume.", flush=True)
            return
    print("All questions answered.", flush=True)

if __name__ == "__main__":
    main()
