"""Produce DRAFT English transcripts for the game's recorded voice clips.

Requires pip install faster-whisper. Run in the CI transcription workflow:
    python tools/transcribe_recorded_voice.py --groups challenge_dialogue \
        --output analysis/draft_transcripts_challenge.json

This NEVER translates or edits a shipped language file. Automatic speech recognition
is fallible, especially with Dr. Bastard's effects, overlapping sound, names,
accents and music. Each draft must be listened to and corrected by a person.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from voice_inventory import ROOT, inventory


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--groups", help="comma-separated voice groups; default: all except encyclopedia previews")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--model", default="small.en", help="Whisper English model, e.g. base.en or small.en")
    p.add_argument("--limit", type=int, default=0, help="for a short smoke test")
    args = p.parse_args()

    groups = set(args.groups.split(",")) if args.groups else None
    clips = [x for x in inventory()
             if x["group"] != "encyclopedia_preview"
             and (groups is None or x["group"] in groups)]
    if args.limit:
        clips = clips[:args.limit]
    if not clips:
        raise SystemExit("No clips selected")
    print(f"Transcribing {len(clips)} recordings with {args.model}", flush=True)

    from faster_whisper import WhisperModel
    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type="int8",
        cpu_threads=min(4, os.cpu_count() or 2),
        num_workers=1,
    )
    output = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(clips, start=1):
        filename = ROOT / item["path"]
        if not filename.is_file():
            raise FileNotFoundError(f"Missing sound asset: {filename}")
        segments, info = model.transcribe(
            str(filename),
            language="en",
            beam_size=5,
            best_of=5,
            condition_on_previous_text=False,
            initial_prompt="AudioDefence: Zombie Arena. Dr. Bastard. Zombies. Snufflehog. Berserk. Maya.",
            vad_filter=False,
        )
        segs = list(segments)
        candidate = " ".join(s.text.strip() for s in segs).strip()
        output.append({
            "path": item["path"],
            "key": item["key"],
            "group": item["group"],
            "seconds": item["seconds"],
            "english_draft": candidate,
            "segments": [{"start": round(s.start, 2), "end": round(s.end, 2),
                          "text": s.text.strip(),
                          "avg_logprob": round(s.avg_logprob, 3),
                          "no_speech_prob": round(s.no_speech_prob, 3)} for s in segs],
            "human_reviewed": False,
            "vietnamese": "",
            "translation_reviewed": False,
        })
        if index % 5 == 0 or index == len(clips):
            print(f"{index}/{len(clips)} transcribed; {item['group']} {item['key']}", flush=True)
            args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8")

    print(f"Draft complete: {len(output)} items, NOT reviewed translations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
