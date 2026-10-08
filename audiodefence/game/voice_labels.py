"""Vietnamese spoken companions for short, unambiguous original voice callouts.

Unlike longer Dr. Bastard recordings, these sound keys explicitly identify a
spoken weapon, power-up, or immediate instruction. Labels describe what is said,
but are NOT claimed to be verified word-for-word recordings.

Only the *recorded voice clip* is made quieter. The zombie, weapon, ambient,
HRTF and gameplay sounds retain their original gain.
"""
from __future__ import annotations

# Original audio key -> short Vietnamese text for the game's TTS voice.
LABELS = {
    "announcer_outofammo_c": "Hết đạn!",
    "announcer_reload_b": "Nạp đạn!",
    "announcer_reload_g": "Nạp đạn!",
    "weapon_gun_bazooka_voice": "Súng phóng rocket.",
    "weapon_gun_grenade_voice": "Súng phóng lựu.",
    "weapon_gun_hunting_voice": "Súng trường săn.",
    "weapon_gun_machinegun_voice": "Súng máy.",
    "weapon_gun_microsmg_voice": "Tiểu liên Micro SMG.",
    "weapon_gun_pistol_voice": "Súng lục.",
    "weapon_gun_policeshotgun_voice": "Shotgun cảnh sát.",
    "weapon_gun_sawnoff_voice": "Shotgun nòng ngắn.",
    "weapon_gun_sonic_voice": "Pháo âm thanh.",
    "weapon_gun_tactical_voice": "Súng trường chiến thuật.",
    "fireworks_announce": "Pháo hoa!",
    "minigun_announce": "Súng máy Minigun!",
    "tesla_announce": "Trường điện Tesla!",
    "tornado_announce": "Lốc xoáy!",
    "fireworks_announce_b": "Pháo hoa!",
    "minigun_announce_c": "Súng máy Minigun!",
    "tesla_announce_a": "Trường điện Tesla!",
    "tornado_announce_a": "Lốc xoáy!",
}


def companion_label(key: str | None) -> str | None:
    key = key or ""
    label = LABELS.get(key)
    if label:
        return label
    # All long Challenge dialogue goes through ADSound so it can hold its
    # wave and implement skip/pause. Read other recordings here at the
    # central sound-play event: game-over, revive, opener, tutorial help.
    if key.startswith("bastard_") and not key.startswith("bastard_gameover_"):
        return None
    from .voice_drafts_vi import draft_for
    if key.startswith(("bastard_gameover_", "OPENER_", "revive_",
                        "announcer_revive", "announcer_tutorial_aimhelp",
                        "announcer_tutorial_aimprompt")):
        return draft_for(key)
    return None


def speak_short_voice(sound) -> bool:
    """Read a Vietnamese companion once when its *original* speech clip plays.

    On other languages and platforms nothing changes. TTS does not replace the
    recording, and ends up in the game's separate speech mix.
    """
    from ..platform import host
    if not host.ANDROID or sound is None:
        return False
    from .parameters import GameParameters
    params = GameParameters.shared()
    if params.language() != "Tiếng Việt":
        return False
    key = getattr(sound, "key", None) or ""
    # Announcer Off only suppresses call-outs the game already suppresses,
    # not a scripted game-over line or the opening film.
    if key in LABELS and not params.last_announcer_value():
        return False
    text = companion_label(key)
    if not text:
        return False

    from ..platform.speech import Speech
    # The same agent can be reused. Keep the original gain for the engine's
    # normal stop/cleanup path to restore. Do NOT register an end callback here:
    # the sound dispatcher gives each sound one monitor and registering another
    # would erase power-up activation or challenge completion callbacks.
    original_gain = getattr(sound, "_vi_voice_original_gain", None)
    if original_gain is None:
        original_gain = sound.gain
        sound._vi_voice_original_gain = original_gain
    sound.set_gain(original_gain * 0.32)
    Speech.shared().speak_in_game(text, False)
    return True
