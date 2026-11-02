"""Blind test, round 2: re-run only the Chair on the saved round-1 meetings, using the new resolution format.

The members' statements and cross-examination are reused unchanged, so the only difference is the Chair's write-up.
"""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent
NEW_APP = Path(sys.argv[1])
sys.path.insert(0, str(NEW_APP))
import boardroom as br

MEETINGS = HERE / "app" / "data" / "meetings"
ANSWERS = json.loads((HERE / "answers.json").read_text(encoding="utf-8"))
OUT = HERE / "answers_v2.json"
board = json.loads((HERE / "app" / "members.json").read_text(encoding="utf-8"))
chair_system = json.loads((NEW_APP / "members.json").read_text(encoding="utf-8"))["chair"]["brief"]
model = board.get("model", "sonnet")

def rechair(key):
    q = ANSWERS[key]
    m = json.loads((MEETINGS / f"{q['board']['meeting_id']}.json").read_text(encoding="utf-8"))
    ok = [s for s in m["statements"] if s.get("ok")]
    for attempt in range(2):
        res = br.ask_claude(chair_system, br.chair_prompt(m["agenda"], m.get("context", ""), ok, m.get("reviews") or []), [], model)
        if res.get("ok"):
            return {"ok": True, "text": res["text"], "seconds": res.get("seconds"), "meeting_id": m["id"]}
        time.sleep(5)
    return {"ok": False, "error": res.get("error")}

results = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
todo = [k for k in ANSWERS if not results.get(k, {}).get("ok")]
with ThreadPoolExecutor(3) as pool:
    for k, r in zip(todo, pool.map(rechair, todo)):
        results[k] = r
        print(f"[{time.strftime('%H:%M:%S')}] Q{k}: ok={r['ok']}", flush=True)
        OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print("Done.", flush=True)
