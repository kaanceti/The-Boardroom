"""Build docs/index.html: a no-install demo that replays saved meetings in the browser (for GitHub Pages).

    python tools/build_demo.py . benchmark/round3/meetings/<id>.json ... docs/index.html
"""
import json, shutil, sys
from pathlib import Path

app = Path(sys.argv[1])          # folder with static/index.html and members.json
meetings_files = [Path(p) for p in sys.argv[2:-1]]
out = Path(sys.argv[-1])

html = (app / "static" / "index.html").read_text(encoding="utf-8")
board = json.loads((app / "members.json").read_text(encoding="utf-8"))
public_board = {"chair": {k: board["chair"].get(k) for k in ("id", "name", "speciality", "model")},
                "members": [{k: m.get(k) for k in ("id", "name", "speciality", "model")} for m in board["members"]]}
meetings = []
for f in meetings_files:
    m = json.loads(f.read_text(encoding="utf-8"))
    keep = {k: m.get(k) for k in ("id", "title", "agenda", "context", "mode", "created", "statements", "reviews", "resolution", "verdict")}
    line = keep["agenda"].strip().splitlines()[0]
    keep["title"] = line if len(line) <= 80 else line[:80].rsplit(" ", 1)[0].rstrip(" ,;:") + "…"
    keep["statements"] = [{k: s.get(k) for k in ("id", "name", "speciality", "model", "ok", "text", "seconds")} for s in m["statements"]]
    keep["reviews"] = [{k: r.get(k) for k in ("id", "name", "ok", "text", "seconds")} for r in (m.get("reviews") or [])]
    keep["resolution"] = {k: (m.get("resolution") or {}).get(k) for k in ("ok", "text", "model")}
    meetings.append(keep)

# The office cat: its brain runs in the page, so the demo cat can talk too (starter brain, public text only).
cat_js = app / "cat" / "tinycat.js"
starter = app / "cat" / "starter-brain.json"
sys.path.insert(0, str(app / "cat"))
try:
    import prepare, safety
    cat_topics = [{"id": m["id"], "topic": t} for m in meetings
                  for t in [prepare.topic_of(m["agenda"])] if t and safety.safe(t)]
except ImportError:
    cat_topics = []

demo_js = r'''
// ---- Demo mode: no server. Saved meetings replay as if they were happening now. ----
const DEMO = __DATA__;
const demoStart = {};
const sleep = ms => new Promise(r => setTimeout(r, ms));
function demoState(m) {
  const t = (Date.now() - (demoStart[m.id] ??= Date.now())) / 1000;
  const s = JSON.parse(JSON.stringify(m));
  const n = s.statements.length;
  s.statements = s.statements.map((x, i) => t >= 2 + 1.6 * i ? { ...x, status: "done" } : { id: x.id, name: x.name, speciality: x.speciality, status: "thinking" });
  let end = 2 + 1.6 * (n - 1);
  const hasReviews = (s.reviews || []).length > 0;
  if (hasReviews) {
    const r0 = end + 1.2;
    s.reviews = t < r0 ? [] : s.reviews.map((x, i) => t >= r0 + 1 + 1.1 * i ? { ...x, status: "done" } : { id: x.id, name: x.name, status: "thinking" });
    end = r0 + 1 + 1.1 * (s.reviews.length - 1);
  }
  const c0 = end + 1.2;
  s.resolution = t < c0 ? null : t < c0 + 3 ? { status: "thinking" } : { ...m.resolution, status: "done" };
  const allDone = s.statements.every(x => x.status === "done");
  s.stage = !allDone ? "statements" : hasReviews && t < c0 ? "review" : t < c0 + 3 ? "resolution" : "done";
  return s;
}
const api = async (p, opts) => {
  await sleep(80);
  if (p === "/api/board") return DEMO.board;
  if (p === "/api/faces") return {};
  if (p === "/api/cat") return DEMO.cat;
  if (p === "/api/status") return { ok: true, message: "Demo: replaying saved meetings" };
  if (p === "/api/meetings" && opts && opts.method === "POST")
    return { error: "This demo replays saved meetings. Download The Boardroom from GitHub to ask your own questions." };
  if (p === "/api/meetings") return DEMO.meetings.map(m => ({ id: m.id, title: m.title, created: m.created, stage: "done", mode: m.mode, verdict: m.verdict && m.verdict.call }));
  const id = p.split("/").pop();
  const m = DEMO.meetings.find(x => x.id === id);
  return m ? demoState(m) : { error: "Meeting not found" };
};
'''.replace("__DATA__", json.dumps({"board": public_board, "meetings": meetings,
                                 "cat": {"brain": "starter" if starter.exists() else None, "topics": cat_topics,
                                         "learning": {"running": False}, "auto": False,
                                         "blocked": list(getattr(sys.modules.get("safety"), "BLOCKED", []))}}, ensure_ascii=False))

def rep(s, old, new):
    assert s.count(old) == 1, (old[:70], s.count(old))
    return s.replace(old, new)

html = rep(html, 'const api = (p, opts) => fetch(p, opts).then(r => r.json());', demo_js)
# replay faster than the real app polls, and restart a replay when a meeting is clicked
html = rep(html, 'if (m.stage !== "done") pollTimer = setTimeout(() => openMeeting(id), 2500);',
                 'if (m.stage !== "done") pollTimer = setTimeout(() => openMeeting(id), 700);')
html = rep(html, 'el.querySelectorAll("button").forEach(b => b.onclick = () => openMeeting(b.dataset.id));',
                 'el.querySelectorAll("button").forEach(b => b.onclick = () => { delete demoStart[b.dataset.id]; activeTab = null; openMeeting(b.dataset.id); });')
# once the board has walked in, open the first meeting so visitors see it at work
html = rep(html, '  loadMeetings();\n  const st = await api("/api/status");',
                 '  await loadMeetings();\n  await entrance;\n  if (DEMO.meetings.length) openMeeting(DEMO.meetings[0].id);\n  const st = await api("/api/status");')
html = rep(html, '<title>The Boardroom</title>', '<title>The Boardroom (demo)</title>')
html = rep(html, 'const CAN_DOWNLOAD = true;', 'const CAN_DOWNLOAD = false;')
html = rep(html, '<textarea id="agenda" rows="4" placeholder="Ask the board a question or describe a decision" required></textarea>',
                 '<textarea id="agenda" rows="4" placeholder="This demo replays saved meetings. Pick one under Past meetings." required></textarea>')
if cat_js.exists():
    html = rep(html, '<script src="/cat.js"></script>', "<script>\n" + cat_js.read_text(encoding="utf-8") + "</script>")
    html = rep(html, 'const CAT_BRAIN_URL = "/api/cat/brain";', 'const CAT_BRAIN_URL = "cat-brain.json";')
out.parent.mkdir(parents=True, exist_ok=True)
if starter.exists():
    shutil.copyfile(starter, out.parent / "cat-brain.json")
out.write_text(html, encoding="utf-8")
print("wrote", out, len(html), "bytes,", len(meetings), "meetings")
