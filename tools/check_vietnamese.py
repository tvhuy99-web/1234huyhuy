"""Quality checks for the Vietnamese AudioDefence translation.

    python tools/check_vietnamese.py
    python tools/check_vietnamese.py --strict

The normal check is fast: it compares with the previously translated Russian key inventory.
--strict instead extracts every current phrase from source code and game data through
make_language.every_phrase, so it also catches newly introduced strings after a code update.
For additional gameplay coverage, run tools/verify_localization.py --language "Tiếng Việt".
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "localization" / "ru.json"
VIETNAMESE = ROOT / "localization" / "Tiếng Việt.json"

# Values with a format slot must keep the same specifiers. Whitespace after a literal
# percentage is excluded, so "20% faster" is not mistaken for a "% f" placeholder.
FORMAT = re.compile(r"%(?:\d+\$)?[-+#0]*(?:\d+|\*)?(?:\.\d+)?[diufsxc%]")


def unique_pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError("duplicate JSON key: " + key)
        out[key] = value
    return out


def read_json(path: Path):
    with path.open(encoding="utf-8-sig") as fh:
        data = json.load(fh, object_pairs_hook=unique_pairs)
    if not isinstance(data, dict):
        raise ValueError(str(path) + " must contain a JSON object")
    return data


def check(source, translation, strict=False):
    errors = []
    if translation.get("@plural") != "none":
        errors.append('"@plural" must be "none" for Vietnamese')

    source_keys = {k for k in source if not k.startswith("@")}
    actual_keys = {k for k in translation if not k.startswith("@")}
    for key in sorted(source_keys - actual_keys):
        errors.append("missing source key: " + repr(key))
    for key in sorted(actual_keys - source_keys):
        errors.append("unknown key: " + repr(key))

    translated = 0
    untranslated = []
    for key in sorted(source_keys & actual_keys):
        value = translation[key]
        if not isinstance(value, str):
            errors.append("non-string value for: " + repr(key))
            continue
        if not value:
            untranslated.append(key)
            continue
        translated += 1
        if Counter(FORMAT.findall(key)) != Counter(FORMAT.findall(value)):
            errors.append("format parameters changed: " + repr(key))
        if value.count("{") != value.count("}"):
            errors.append("unbalanced plural braces: " + repr(key))
    if strict:
        errors.extend("untranslated: " + repr(key) for key in untranslated)

    return translated, len(source_keys), untranslated, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true", help="check all game/code phrases and require complete translation")
    args = parser.parse_args()
    try:
        translation = read_json(VIETNAMESE)
        if args.strict:
            # The current code and game data are the authority, not another language file.
            # Other existing languages still contribute one-word labels that static extraction misses.
            from make_language import every_phrase
            source = {phrase: '' for phrase in every_phrase(besides=VIETNAMESE.name)}
        else:
            source = read_json(SOURCE)
        done, total, missing, errors = check(source, translation, args.strict)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("Vietnamese localization: " + str(exc), file=sys.stderr)
        return 1

    print(f"Vietnamese: {done}/{total} phrases translated; {len(missing)} to review.")
    for problem in errors[:60]:
        print("ERROR: " + problem, file=sys.stderr)
    if len(errors) > 60:
        print(f"... and {len(errors) - 60} more.", file=sys.stderr)
    if not args.strict and missing:
        print("Partial translation: untranslated phrases fall back to English.")
        print('Run with --strict only when the language is complete.')
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
