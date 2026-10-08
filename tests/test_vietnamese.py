"""Regression tests for Vietnamese speech, placeholders, and menu navigation.

Run: python -m unittest discover -s tests -p 'test_vietnamese.py' -v
"""
from __future__ import annotations

import unittest

from audiodefence import localization
from audiodefence.platform.speech_android import phone_words


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

    def test_english_keyboard_remains_correct(self):
        self.assertEqual(
            localization.translate("Press Enter to select."),
            "Nhấn Enter để chọn.",
        )
        self.assertIn("Chạm đúp", phone_words(localization.translate("Press Enter to select.")))


if __name__ == "__main__":
    unittest.main()
