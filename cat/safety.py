"""Keeps the office cat harmless.

The cat is a toy. It must never sound like legal or medical advice, never swear or insult anyone, and never joke about violence.
So it never learns any of that: cat/prepare.py leaves out every line of training text that matches below.
A model this small mostly repeats and remixes what it learned, so it has no advice or swearing to repeat.
Money talk is allowed: Kibi makes everything up, and the notebook says so under its talk box.
"""
import re

# Lower-case patterns. Kept short on purpose: only what could read as real advice, plus violence and swearing.
BLOCKED = [
    # sounding like advice
    r"\byou should\b", r"\byou must\b", r"\bi recommend", r"\badvi[cs]e", r"\bguarantee",
    # legal and health advice
    r"\blawyer", r"\blegal advice", r"\bsue\b", r"\bdoctor", r"\bmedical\b", r"\bmedication", r"\bpills?\b", r"\bdrugs?\b", r"\bdose",
    r"\bdiagnos", r"\btherap",
    # violence, abuse and self-harm: a silly cat line about these is not a joke (politics and people in the news are fine)
    r"\brap(e|es|ed|ist)\b", r"\bmolest", r"\bpa?edo", r"\bsuicid", r"\bself.?harm", r"\bmurder", r"\bterroris",
    r"\babus(e|ed|er|ive)\b", r"\btortur", r"\bgenocid",
    # swearing and insults
    r"\bfuck", r"\bshit", r"\bbitch", r"\bass\b", r"\basses\b", r"\barse", r"\bdick", r"\bcunt", r"\bbastard",
    r"\bslut", r"\bwhore", r"\bretard", r"\bpiss", r"\bwank", r"\btwat", r"\bprick", r"\bcock", r"\bporn",
]
_RE = re.compile("|".join(BLOCKED))


def safe(text: str) -> bool:
    """True if the cat may say (or learn from) this text."""
    return not _RE.search(text.lower())
