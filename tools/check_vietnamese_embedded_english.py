"""Detect untranslated *English fragments inside Vietnamese strings*.

A nonempty translation is not enough: a Vietnamese sentence such as
"Đã lưu. Please try again." has a nonempty translated value but still
reads an English clause to the player. We examine every saved UI value,
every TTS draft keyed to an English voice recording, and short voice labels.

The heuristic intentionally does not reject English loanwords, names and
controls such as "zombie", "game", "menu", "Enter", "Escape", "Dr. Bastard",
"Audio Defence", "OpenAL" or file paths. Nor does it pretend to certify
the *meaning* of each ASR transcription: that requires listening review.

    python tools/check_vietnamese_embedded_english.py
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

# Words signalling English sentence structure, instructions, and states.
# Exclude "game", "menu", "may", "do", "else", "in" and "on", which
# occur as Vietnamese words or product/navigational terminology.
ENGLISH = frozenset("""
the and but with from you your yours yourself we our they them their theirs
this that these those there where when while because which would should could
will must please press tap click swipe wait select choose continue previous
warning error loading complete failed success already were have has does into
without until unless though behind between through against more before after
anyone someone nothing everything somebody nobody something anything every
again instead actually here's you're i've i'm it's you'll won't don't isn't
aren't weren't haven't doesn't didn't ready sorry thanks thank hello goodbye
not retry reload shoot fire restart cancel unavailable welcome later
""".split())
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)

# A complete English instruction may have no articles; catch those as well.
ENGLISH_PHRASE = re.compile(
    r"(?<!\w)(?:game over|level up|try again|thank you|good luck|new game|"
    r"main menu|press enter|press escape|please wait|not available|"
    r"your [a-z]{3,}|you [a-z]{3,}|the [a-z]{3,})(?!\w)",
    re.IGNORECASE,
)


def suspect_fragments(vietnamese: str) -> list[str]:
    """Return high-confidence English grammar tokens and short clauses.

    A name containing only ASCII letters is *not* an English sentence. Use
    Unicode-aware word boundaries to avoid detecting "a" in "của" or "n"
    in "nhấn", which happened with naive [A-Za-z]+ scanning.
    """
    found = []
    for match in WORD.finditer(vietnamese):
        word = match.group(0)
        if word.isascii() and word.lower() in ENGLISH:
            found.append(word)
    found.extend(m.group(0) for m in ENGLISH_PHRASE.finditer(vietnamese))
    return list(dict.fromkeys(found))


# Even a fragment with no function words ("Zombies attack now") can be an
# untranslated English sentence if it is copied verbatim from the source.
# Ignore technical strings and credit names which should remain unchanged.
NON_SPEECH = re.compile(
    r"github\.com/[^\s,;]+|AudioDefence backup\.zip|"
    r"\b(?:Loh Boon Keat|Wong Wee Xiang|Muhammad Hajjar|Somethin' Else|Papa Sangre)\b|"
    r"%(?:\d+\$)?[-+#0-9.]*[diufsxc%]|[\w.-]+\.(?:json|zip|mhr|sofa)",
    re.IGNORECASE,
)


def repeated_source_phrases(source: str, translated: str) -> list[str]:
    """Find 3+ English source words copied as an uninterrupted phrase.

    Requires the original English source, so this check only applies to
    localization JSON; prerecorded dialogue drafts have no verified English
    transcripts in the source tree. The independent function-word check
    still examines all voice drafts.
    """
    original = [m.group(0).lower() for m in WORD.finditer(NON_SPEECH.sub(" ", source))]
    target = [m.group(0).lower() for m in WORD.finditer(NON_SPEECH.sub(" ", translated))]
    source_groups = {tuple(original[i:i+3]) for i in range(len(original)-2)}
    return sorted({" ".join(target[i:i+3]) for i in range(len(target)-2)
                   if tuple(target[i:i+3]) in source_groups})


def literals_from(path: Path, variable: str) -> dict[str, str]:
    """Read a dict and any .update(dict) calls *without importing game code*."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == variable
                for target in node.targets):
            items = ast.literal_eval(node.value)
            found.update(items)
        elif (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
              and isinstance(node.value.func, ast.Attribute)
              and isinstance(node.value.func.value, ast.Name)
              and node.value.func.value.id == variable
              and node.value.func.attr == "update" and len(node.value.args) == 1):
            found.update(ast.literal_eval(node.value.args[0]))
    return found


def audit() -> tuple[int, list[str]]:
    vi_path = ROOT / "localization" / "Tiếng Việt.json"
    localization = json.loads(vi_path.read_text(encoding="utf-8"))
    voice_drafts = literals_from(ROOT / "audiodefence/game/voice_drafts_vi.py",
                                 "ASR_DRAFT_VI")
    voice_labels = literals_from(ROOT / "audiodefence/game/voice_labels.py",
                                 "LABELS")
    groups = (
        ("localization", {k: v for k, v in localization.items() if not k.startswith("@")}),
        ("recorded-voice TTS", voice_drafts),
        ("short-voice TTS", voice_labels),
    )
    total = 0
    problems = []
    for category, items in groups:
        for key, value in items.items():
            total += 1
            if not isinstance(value, str):
                problems.append(f"{category}: {key!r} has non-string value")
                continue
            hits = suspect_fragments(value)
            # The English original is the JSON key, never the voice filename.
            # Compare copied *word sequences* as well as grammar markers.
            if category == "localization":
                hits.extend(repeated_source_phrases(key, value))
            if hits:
                problems.append(f"{category}: {key[:95]!r}: {hits!r} in {value[:150]!r}")
        print(f"{category}: {len(items)} values reviewed for embedded English clauses.")
    return total, problems


def main() -> int:
    total, problems = audit()
    print(f"Embedded-English audit: {total} strings checked, {len(problems)} suspected clauses.")
    for line in problems[:45]:
        print("ERROR: " + line, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
