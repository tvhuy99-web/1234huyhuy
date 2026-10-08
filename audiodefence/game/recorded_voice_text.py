"""Short, contextual Vietnamese companion lines for *identified* recorded Challenge speech.

These are deliberately concise descriptions of what the recording announces, not claimed
word-for-word transcripts. They reuse English game text whose Vietnamese version already
lives in localization/Tiếng Việt.json.

Each key is the ORIGINAL sound's basename (without .m4a). Only explicitly reviewed,
speech-bearing sound keys appear here. Do not guess words for unknown recordings: there
is no corresponding transcript for most Dr. Bastard recordings in the original plists.

The existing tutorial_announcer is handled by tutorial_text.py separately and MUST NOT
be duplicated here. This file is harmless outside Android Vietnamese mode.
"""
from __future__ import annotations

#: Sound key -> existing English game phrase, which is translated at the moment of speaking.
#: This companion can be shorter than the actor's line so it does not cover gameplay sounds.
CHALLENGE_VOICE_LINES = {
    'bastard_passerby_storm_a': 'Rain and random thunder hinder your hearing.',
    'bastard_passerby_cows_a': "A herd of cows is pasturing in the arena! They'll get in the way of shooting zombies.",
    'bastard_passerby_cars_a': 'Car alarms will go off around you. Shoot the cars to blow them up!',
    'bastard_passerby_jukebox_a': 'An old jukebox keeps playing terrible music. Shoot it to stop it!',
    'bastard_zombie_horde_c': "Get ready! Dr. Bastard has unleashed a zombie horde! They'll come at you from all directions!",
    'bastard_zombie_shield_a': 'The newest creation of Dr. Bastard comes with an invincible shield! Watch out!',
    'bastard_zombie_hulk_a': "The Hulk is a bullet sponge and will close in fast when you're reloading. Switching to your other gun is the fastest way to keep shooting at him.",
    'bastard_zombie_runner_a': 'The Snufflehog is the fastest Zombie in the game. Shoot it the moment you hear one coming!',
    'bastard_zombie_berserk_a': "You don't want to shoot the Berserk. If you hear a Zombie sniffing around, avoid shooting it at all costs! It will go away in a few seconds.",
    'bastard_zombie_whisperer_a': 'Listen very carefully! The Whisperer moves very quietly!',
    'bastard_zombie_clown_a': 'Clowns move around you in large circles and take ages to get to you. Always focus on other zombies first.',
}


def companion_for(sound_key: str | None) -> str | None:
    """An English phrase to send through normal localization, or None if not reviewed."""
    return CHALLENGE_VOICE_LINES.get(sound_key or '')
