"""Regression tests for Vietnamese speech, placeholders, and menu navigation.

Run: python -m unittest discover -s tests -p 'test_vietnamese.py' -v
"""
from __future__ import annotations

import unittest

from audiodefence import localization
from audiodefence.platform.speech_android import phone_words
from audiodefence.game.recorded_voice_text import CHALLENGE_VOICE_LINES, companion_for
from audiodefence.game.voice_labels import LABELS, companion_label
from audiodefence.game.voice_drafts_vi import ASR_DRAFT_VI, draft_for
from pathlib import Path


class VietnameseSpeechTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not localization.load("Tiếng Việt", force=True):
            raise RuntimeError("Tiếng Việt.json could not be loaded")

    @classmethod
    def tearDownClass(cls):
        localization.load(localization.ENGLISH, force=True)

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
        self.assertGreaterEqual(len(ASR_DRAFT_VI), 71)
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
