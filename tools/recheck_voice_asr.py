"""Reproduce an offline English ASR pass without changing Vietnamese captions.

Optional dependencies: faster-whisper, numpy, and the ffmpeg executable.
The model cache is supplied by the caller. ASR output is never marked as
human-verified, and an empty result does not prove an asset is an effect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from voice_inventory import ROOT, inventory, _load_module, DRAFT_VI


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", required=True, help="model name or cached model directory")
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--keys", nargs="+", help="default: all 114 drafts plus revive_standby")
    parser.add_argument("--vad", action="store_true")
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--threads", type=int, default=6)
    parser.add_argument("--channel", choices=("mono", "left", "right"), default="mono")
    args = parser.parse_args()

    import numpy as np
    from faster_whisper import WhisperModel

    captions = _load_module(DRAFT_VI, "ad_asr_captions").ASR_DRAFT_VI
    keys = set(args.keys) if args.keys else set(captions) | {"revive_standby"}
    clips = [item for item in inventory() if item["key"] in keys]
    missing = keys - {item["key"] for item in clips}
    if missing:
        parser.error("unknown audio keys: " + ", ".join(sorted(missing)))
    clips.sort(key=lambda item: (item["seconds"], item["key"]))
    model = WhisperModel(args.model, device="cpu", compute_type="int8",
                         cpu_threads=args.threads, num_workers=1,
                         download_root=str(args.cache) if args.cache else None)
    params = dict(language="en", beam_size=5, temperature=0.0,
                  condition_on_previous_text=False, vad_filter=args.vad,
                  initial_prompt=args.prompt)
    if args.vad:
        params["vad_parameters"] = {"min_silence_duration_ms": 500}
    # A pass has one configuration. Never resume a file from different settings.
    done = json.loads(args.output.read_text(encoding="utf-8")) if args.output.exists() else []
    config = dict(model=args.model, parameters=params, channel=args.channel)
    if any(item.get("config") != config for item in done):
        parser.error("existing output uses different settings; use a new output file")
    completed = {item["key"] for item in done}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(clips, 1):
        if item["key"] in completed:
            continue
        filename = ROOT / item["path"]
        cmd = ["ffmpeg", "-v", "error", "-i", str(filename)]
        if args.channel != "mono":
            channel = 0 if args.channel == "left" else 1
            cmd += ["-af", f"pan=mono|c0=c{channel}"]
        cmd += ["-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1"]
        pcm = subprocess.run(cmd, check=True, capture_output=True).stdout
        audio = np.frombuffer(pcm, dtype=np.float32).copy()
        segments, _ = model.transcribe(audio, **params)
        segments = list(segments)
        record = dict(item, config=config,
                      audio_sha256=hashlib.sha256(filename.read_bytes()).hexdigest(),
                      english_asr=" ".join(s.text.strip() for s in segments).strip(),
                      previous_vietnamese=captions.get(item["key"]),
                      human_listened=False,
                      segments=[dict(start=round(s.start, 3), end=round(s.end, 3),
                                     text=s.text.strip(), avg_logprob=round(s.avg_logprob, 4),
                                     no_speech_prob=round(s.no_speech_prob, 4)) for s in segments])
        done.append(record)
        temp = args.output.with_suffix(".tmp")
        temp.write_text(json.dumps(done, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(args.output)
        print(f"{index}/{len(clips)} {item['key']}: {record['english_asr']}", flush=True)


if __name__ == "__main__":
    main()
