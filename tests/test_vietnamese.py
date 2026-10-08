"""Regression tests for Vietnamese speech, placeholders, and menu navigation.

Run: python -m unittest discover -s tests -p 'test_vietnamese.py' -v
"""
from __future__ import annotations

import unittest
from unittest.mock import patch

from audiodefence import localization
from audiodefence.platform.speech_android import phone_words
from audiodefence.game.recorded_voice_text import CHALLENGE_VOICE_LINES, companion_for
from audiodefence.game.voice_labels import LABELS, companion_label
from audiodefence.game.voice_drafts_vi import ASR_DRAFT_VI, draft_for
from audiodefence.game import tutorial_text
from pathlib import Path


class VietnameseSpeechTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not localization.load("Tiếng Việt", force=True):
            raise RuntimeError("Tiếng Việt.json could not be loaded")

    @classmethod
    def tearDownClass(cls):
        localization.load(localization.ENGLISH, force=True)

    def setUp(self):
        # localization.load() changes the loaded table; real phone gesture
        # wording uses the language *selected in settings* instead.
        self._language_patch = patch('audiodefence.localization.language', return_value='Tiếng Việt')
        self._language_patch.start()

    def tearDown(self):
        self._language_patch.stop()

    def test_all_assembled_phone_tutorial_phrases_are_vietnamese(self):
        import json
        phrases = json.loads(Path("localization/Tiếng Việt.json").read_text(encoding="utf-8"))
        values = (list(tutorial_text.PHONE_AIM.values()) +
                  list(tutorial_text.PHONE_LINES.values()) +
                  list(tutorial_text.PHONE_BUTTON_LINES.values()) +
                  [tutorial_text.PAD_AIM, tutorial_text.PAD_AIM_BUTTONS,
                   tutorial_text.PAD_SHAKE])
        self.assertEqual(len(values), 16)
        for english in values:
            with self.subTest(english=english):
                self.assertIn(english, phrases, "Spoken tutorial text lacks a translation key")
                self.assertTrue(phrases[english].strip())
                self.assertNotEqual(localization.translate(english), english)
        # The tutorial dynamically chooses the phone's aiming mode.
        with patch.object(tutorial_text.host, 'ANDROID', True):
            from audiodefence.game.parameters import GameParameters
            with patch.object(GameParameters, 'shared') as shared:
                shared.return_value.control_scheme = 1
                shared.return_value.button_mode = False
                self.assertEqual(
                    localization.translate(tutorial_text.phone_text_for("announcer_tutorial_aim_gyroMode")),
                    phrases[tutorial_text.PHONE_AIM[1]],
                )
                shared.return_value.button_mode = True
                self.assertEqual(
                    localization.translate(tutorial_text.phone_text_for("announcer_tutorial_reload_buttonMode")),
                    phrases[tutorial_text.PHONE_BUTTON_LINES['reload']],
                )

    def test_english_gesture_keeps_english_words(self):
        with patch('audiodefence.localization.language', return_value=localization.ENGLISH):
            self.assertEqual(phone_words('Press Escape to cancel.'), 'Press a two-finger scrub to cancel.')
            self.assertEqual(phone_words('Press Enter to select.'), 'Double tap to select.')
            self.assertEqual(phone_words('Shift + Enter to go back.'), 'double tap and hold to go back.')
            self.assertNotIn('ngón', phone_words('Escape on the keyboard'))

    def test_game_offers_vietnamese(self):
        self.assertIn("Tiếng Việt", localization.available())

    def test_menu_and_gameplay_phrases(self):
        self.assertEqual(localization.translate("Play"), "Chơi")
        self.assertEqual(localization.translate("Endless"), "Vô tận")
        self.assertEqual(localization.translate("Reload"), "Nạp đạn")
        self.assertEqual(localization.translate("Armory"), "Kho vũ khí")

    def test_numeric_placeholder(self):
        self.assertEqual(
            localization.translate("You need 15 stars to play this level"),
            "Bạn cần 15 sao để chơi màn này",
        )

    def test_plural_suffix_does_not_spoil_vietnamese(self):
        self.assertEqual(localization.translate("2 stars unlocked"), "Đã mở khóa 2 sao")
        self.assertEqual(localization.translate("1 star unlocked"), "Đã mở khóa 1 sao")

    def test_android_double_tap(self):
        self.assertEqual(phone_words("Nhấn Enter để chọn."), "Chạm đúp để chọn.")

    def test_android_double_tap_and_hold(self):
        self.assertEqual(
            phone_words("Nhấn Enter để đến thiết lập tiếp theo, Shift cộng Enter để quay lại."),
            "Chạm đúp để đến thiết lập tiếp theo, chạm đúp và giữ để quay lại.",
        )

    def test_android_back_gesture(self):
        self.assertEqual(
            phone_words("Nhấn Escape để hủy."),
            "Vuốt qua lại bằng hai ngón để hủy.",
        )

    def test_recorded_voice_companion_only_for_reviewed_cues(self):
        # Unknown recordings must not be given an invented translation.
        self.assertIsNone(companion_for('bastard_tutorial_1_1'))
        self.assertIsNone(companion_for('announcer_tutorial_reload_buttonMode'))
        self.assertGreaterEqual(len(CHALLENGE_VOICE_LINES), 10)
        for key, english_text in CHALLENGE_VOICE_LINES.items():
            with self.subTest(key=key):
                self.assertTrue(english_text)
                self.assertNotEqual(localization.translate(english_text), english_text)
                # Each entry must match an actual recorded sound in the game data.
                path = Path('game/sounds/challenges')
                self.assertTrue(
                    any(path.glob('*/' + key + '.m4a')),
                    'No corresponding recording found for ' + key,
                )

    def test_asr_draft_coverage_is_declared_not_verified(self):
        import json
        inventory = json.loads(Path("analysis/voice_inventory.json").read_text(encoding="utf-8"))
        mapped = {item["key"] for item in inventory}
        self.assertGreaterEqual(len(ASR_DRAFT_VI), 114)
        challenge_clips = {item["key"] for item in inventory
                           if item["group"] == "challenge_dialogue"}
        self.assertEqual(len(challenge_clips), 88)
        self.assertTrue(challenge_clips.issubset(ASR_DRAFT_VI),
                        "Every recorded Challenge dialogue requires Vietnamese text")
        for key, vietnamese in ASR_DRAFT_VI.items():
            with self.subTest(voice_key=key):
                self.assertIn(key, mapped, "Translation refers to unknown audio")
                self.assertTrue(vietnamese.strip())
                # A brand title such as "Audio Defence!" may legitimately
                # contain no accented Vietnamese characters.
                self.assertTrue(any(ord(char) > 127 for char in vietnamese)
                                or vietnamese == "Audio Defence!")
                self.assertEqual(draft_for(key), vietnamese)
        for clip in inventory:
            if clip["status"] == "asr_draft_vi_needs_review":
                self.assertIn(clip["key"], ASR_DRAFT_VI)
                self.assertFalse(clip["verified_transcript"])
        self.assertIsNone(draft_for("ambient_arena"))

    def test_short_spoken_labels_match_audio_files(self):
        sound_paths = Path("analysis/data/sounds.tsv").read_text(encoding="utf-8").splitlines()[1:]
        sound_stems = {Path(line.split("\t", 1)[0]).stem for line in sound_paths}
        self.assertGreaterEqual(len(LABELS), 21)
        for key, translated in LABELS.items():
            with self.subTest(sound=key):
                self.assertIn(key, sound_stems, "No corresponding original sound asset")
                self.assertTrue(translated.strip())
                self.assertEqual(companion_label(key), translated)
        self.assertIsNone(companion_label("weapon_gun_pistol_fire_a"))

    def test_english_keyboard_remains_correct(self):
        self.assertEqual(
            localization.translate("Press Enter to select."),
            "Nhấn Enter để chọn.",
        )
        self.assertIn("Chạm đúp", phone_words(localization.translate("Press Enter to select.")))


if __name__ == "__main__":
    unittest.main()
