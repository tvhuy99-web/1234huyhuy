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

    def test_no_english_subsentences_inside_vietnamese_ui_or_tts(self):
        from tools.check_vietnamese_embedded_english import suspect_fragments, audit
        # A translation with a Vietnamese prefix is *still incomplete* if
        # its second sentence, or even a two-word command, remains English.
        for sample in (
            "Đã lưu. Please try again.",
            "Chú ý! The zombie is behind you.",
            "Bạn có thể tiếp tục, press Enter to select.",
            "Trò chơi kết thúc. Game over.",
            "Đã tới nơi. Reload your weapon!",
        ):
            with self.subTest(untranslated=sample):
                self.assertTrue(suspect_fragments(sample))
        for valid in (
            "Tiến sĩ Bastard giới thiệu zombie Hulk.",
            "Nhấn Enter để quay lại menu. Game vẫn giữ dữ liệu cũ.",
            "Mở tệp AudioDefence backup.zip trong Documents.",
            "Của ai? Có lẽ là Papa Sangre.",
            "Nạp đạn, rồi trở lại đấu trường!",
        ):
            with self.subTest(approved=valid):
                self.assertEqual(suspect_fragments(valid), [])
        total, issues = audit()
        self.assertGreaterEqual(total, 1651)
        self.assertEqual(issues, [])

    def test_all_assembled_phone_tutorial_phrases_are_vietnamese(self):
        # AST audit: importing tutorial_text would pull pygame into a
        # lightweight localization test runner unnecessarily.
        import ast
        import json
        tree = ast.parse(Path("audiodefence/game/tutorial_text.py").read_text(encoding="utf-8"))
        phrases = json.loads(Path("localization/Tiếng Việt.json").read_text(encoding="utf-8"))
        wanted = {"PHONE_AIM", "PHONE_LINES", "PHONE_BUTTON_LINES",
                  "PAD_AIM", "PAD_AIM_BUTTONS", "PAD_SHAKE"}
        found = {}
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    found[target.id] = ast.literal_eval(node.value)
        self.assertEqual(set(found), wanted)
        values = [text for name in wanted for text in
                  (found[name].values() if isinstance(found[name], dict) else [found[name]])]
        self.assertEqual(len(values), 16)
        for english in values:
            with self.subTest(english=english):
                self.assertIn(english, phrases, "Spoken tutorial text lacks a translation key")
                self.assertTrue(phrases[english].strip())
                self.assertNotEqual(localization.translate(english), english)

    def test_about_credits_retain_names_but_not_english_roles(self):
        import ast
        tree = ast.parse(Path("audiodefence/ui/credits_text.py").read_text(encoding="utf-8"))
        values = {}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in (
                            "STUDIO_TEXT", "CREDITS_TEXT", "PORT_CREDITS_TEXT"):
                        values[target.id] = ast.literal_eval(node.value)
        self.assertEqual(len(values), 3)
        translated = localization.translate(values["STUDIO_TEXT"] + values["CREDITS_TEXT"])
        translated += localization.translate(values["PORT_CREDITS_TEXT"])
        for english in (
            "Original Idea & Game Design", "Executive Producers", "by Somethin' Else",
            "The Windows and Mac port", "Ported by", "Built from the game's own code",
            "is Somethin' Else's, and this port only carries it to a keyboard."):
            with self.subTest(english=english):
                self.assertNotIn(english, translated)
        self.assertIn("Loh Boon Keat", translated)  # creator name is not translated

    def test_all_dynamic_keyboard_tutorial_lines_translate(self):
        import ast
        tree = ast.parse(Path("audiodefence/game/tutorial_text.py").read_text(encoding="utf-8"))
        lines = None
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "LINES" for t in node.targets):
                lines = ast.literal_eval(node.value)
                break
        self.assertIsNotNone(lines)
        self.assertEqual(len(lines), 7)
        actions = dict.fromkeys(("turn_left", "turn_right", "fire", "reload",
                                 "pause", "next_weapon", "skip", "melee"), "Enter")
        for topic, english in lines.items():
            with self.subTest(topic=topic):
                spoken = english.format(**actions)
                translated = localization.translate(spoken)
                self.assertNotEqual(translated, spoken, "Dynamic keyboard hint remains English")
                self.assertTrue(any(ord(ch) > 127 for ch in translated))

    def test_android_menu_touch_words_stay_vietnamese(self):
        # The in-game menu hint converter uses a keyboard-independent table.
        # Inspect its patterns without importing pygame/controller hardware.
        import ast
        import re
        tree = ast.parse(Path("audiodefence/platform/pad.py").read_text(encoding="utf-8"))
        matches = [node for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "_TOUCH_WORDS_VI"
                           for t in node.targets)]
        self.assertEqual(len(matches), 1)
        rules = ast.literal_eval(matches[0].value)
        for original, expected in (
            ("Nhấn Enter để chọn.", "Chạm đúp để chọn."),
            ("Nhấn Escape để hủy.", "Vuốt qua lại bằng hai ngón để hủy."),
            ("Shift cộng Enter để quay lại.", "chạm đúp và giữ để quay lại."),
        ):
            said = original
            for pattern, words in rules:
                said = re.sub(pattern, words, said)
            self.assertEqual(said, expected)

    def test_native_android_startup_speaks_saved_vietnamese(self):
        # Native Java runs before Python is initialized. These announcements
        # must not bypass the game language from the previous session.
        java = Path("android/app/src/main/java/com/audiodefence/MainActivity.java").read_text(
            encoding="utf-8")
        self.assertIn('new File(home, "AudioDefence")', java)
        self.assertIn('"settings.json"', java)
        self.assertIn('new JSONObject(value.toString())', java)
        self.assertIn('saved.optString("language"', java)
        self.assertIn('bridge.setGameSpeechLanguage(bootVietnamese ? "vi-VN" : "")', java)
        self.assertIn('vietnameseForStartup(home)', java)
        self.assertIn('"Đang chuẩn bị dữ liệu trò chơi.', java)
        self.assertIn('"Đang giải nén bản cập nhật."', java)
        self.assertIn('"Trò chơi đã sẵn sàng."', java)
        self.assertIn('"TalkBack đang bật.', java)
        self.assertIn('"Xin lỗi, trò chơi không thể khởi động.', java)
        self.assertIn('" phần trăm"', java)

    def test_default_voice_hints_for_both_desktop_systems(self):
        import ast
        import json
        tree = ast.parse(Path("audiodefence/ui/settings.py").read_text(encoding="utf-8"))
        vi = json.loads(Path("localization/Tiếng Việt.json").read_text(encoding="utf-8"))
        nodes = [node for node in tree.body if isinstance(node, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == "VOICE_DEFAULT_HINT"
                         for t in node.targets)]
        self.assertEqual(len(nodes), 1)
        versions = [item.value for item in ast.walk(nodes[0].value)
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)]
        self.assertEqual(len(versions), 2)
        for english in versions:
            with self.subTest(english=english):
                self.assertIn(english, vi)
                self.assertNotEqual(localization.translate(english), english)

    def test_tarot_shuffle_price_read_in_vietnamese(self):
        sentence = "%i diamonds and %i coins. You have %i diamonds and %i coins" % (
            5, 200, 8, 1000)
        translated = localization.translate(sentence)
        self.assertIn("Giá xáo bài", translated)
        self.assertIn("Bạn hiện có", translated)
        self.assertIn("1000", translated)
        self.assertNotIn("You have", translated)
        self.assertEqual(localization.translate("Free while testing"),
                         "Miễn phí khi thử nghiệm")

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
