"""Supplementary audit of English text assembled from Python constants.

The main localization verifier walks UI constructors and game data. This
supplement catches sentence-like literals assigned to descriptive variables,
including dictionaries which only become spoken after runtime assembly.

This is a REVIEW REPORT, not a release certification. Many values are
identifiers, deliberately English proper names, or substrings which the runtime
translator already handles. Review each hit before adding it to JSON.

Run: python tools/audit_vietnamese_dynamic.py
"""
from __future__ import annotations

import ast
from collections import defaultdict
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
VI = ROOT / "localization" / "Tiếng Việt.json"
CODE = ROOT / "audiodefence"
NAME = re.compile(r"(?:text|line|message|label|title|hint|help|description|prompt|notice|instruction|caption|story|speech|words|credit|tip)", re.I)
ENGLISH = re.compile(r"\b(?:the|your|you|to|with|from|on|for|in|of|and|press|tap|swipe|shoot|game|weapon|are|when|then|will|can|try|this|please|that)\b", re.I)
NOT_TEXT = re.compile(r"^(?:https?://|www\.)|^[a-zA-Z_][\w.\\/]+\Z", re.I)


def assigned_names(node):
    if isinstance(node, ast.Assign):
        targets = node.targets
        value = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return [], None
    if value is None:
        return [], None
    names = []
    for t in targets:
        if isinstance(t, ast.Name):
            names.append(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            names.extend(e.id for e in t.elts if isinstance(e, ast.Name))
        elif isinstance(t, ast.Attribute):
            names.append(t.attr)
    return names, value


def main():
    with VI.open(encoding="utf-8") as fh:
        translated = json.load(fh)
    hits = defaultdict(list)
    for path in sorted(CODE.rglob("*.py")):
        if path.name in ("localization.py", "voice_drafts_vi.py", "voice_labels.py",
                         "recorded_voice_text.py") or "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            names, value = assigned_names(node)
            if not names or not any(NAME.search(n) for n in names):
                continue
            for item in ast.walk(value):
                if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                    continue
                for part in item.value.splitlines():
                    phrase = " ".join(part.split())
                    if not 12 <= len(phrase) <= 600 or phrase in translated:
                        continue
                    if NOT_TEXT.match(phrase) or not ENGLISH.search(phrase):
                        continue
                    if not re.search(r"[A-Za-z]{3,}\s+[A-Za-z]{3,}", phrase):
                        continue
                    # Keep probable player-facing phrases. They are suggestions
                    # only: the localization engine may translate parts.
                    hits[phrase].append(f"{path.relative_to(ROOT)}:{item.lineno} ({','.join(names)})")
    print(f"UNCATALOGUED_DYNAMIC_TEXT_CANDIDATES={len(hits)}")
    for phrase, locations in sorted(hits.items(), key=lambda pair: (-len(pair[0]), pair[0].lower()))[:100]:
        print(f"  {phrase[:170]!r} | {locations[0]}")
    if len(hits) > 100:
        print(f"  ... {len(hits)-100} other candidates; not classified as real speech")
    # The report is not authoritative enough to fail the release build.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
