"""A stand-in for the `claude` command, so a whole meeting can run in a test without using anyone's plan.

It answers like a member, a reviewer or the Chair, depending on what it is asked, and writes every prompt it
receives to the file named in FAKE_CLAUDE_LOG, so a test can check exactly what each member was shown.
Members sign their statements on purpose ("**Skeptic's statement**"), as real ones often do.
"""
import json
import os
import re
import sys

args = sys.argv[1:]
if args[:2] == ["auth", "status"]:
    print(json.dumps({"authMethod": "claude.ai"}))
    sys.exit(0)

prompt = sys.stdin.read()
model = args[args.index("--model") + 1] if "--model" in args else "?"
system = ""
if "--system-prompt-file" in args:
    with open(args[args.index("--system-prompt-file") + 1], encoding="utf-8") as f:
        system = f.read()

if "names hidden" in prompt:
    kind = "review"
    labels = sorted(set(re.findall(r"^Statement ([A-Z]):", prompt, re.M)))
    text = "\n".join(f"Statement {label}: strongest point is clear; one claim needs a source." for label in labels)
elif "Write the board's resolution" in prompt:
    kind = "chair"
    text = ("## Decision\nYes, with one condition.\n## Why\nThe numbers work.\n## Main risks\n- Cost overruns.\n"
            "## Next steps\n1. Check the costs.\n## Board notes\n- None\n## Your leaning\nYou wanted a yes.\nVerdict: PARTLY")
else:
    kind = "statement"
    who = re.search(r"You are (.+?), a member of The Boardroom", system)
    name = who.group(1) if who else "Member"
    text = f"**{name}'s statement**\n\nAs the {name}, I think it works.\nBottom line: yes."

log = os.environ.get("FAKE_CLAUDE_LOG")
if log:
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps({"kind": kind, "model": model, "prompt": prompt}) + "\n")
print(json.dumps({"result": text, "is_error": False}))
