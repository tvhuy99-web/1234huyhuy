# Đối chiếu 114 bản dịch lời thu âm — 08/10/2026

**Đã xử lý đủ 114/114 tệp có bản dịch TTS từ ASR.** Mỗi tệp được nhận dạng
lại bằng `large-v3-turbo` và `small.en`, rồi đối chiếu ý nghĩa lời Anh tự
động với bản Việt đang dùng trong game. Đã sửa **8 bản dịch**, giữ **103 bản
dịch** sau đối chiếu, và ghi rõ **3 bản dịch còn mơ hồ**. Tệp chưa có bản
dịch `revive_standby` cũng được nhận dạng riêng.

Đây là đối chiếu văn bản từ nhận dạng giọng nói. Phiên làm việc không hỗ trợ
âm thanh đầu vào để người kiểm tra trực tiếp nghe; **không có tệp nào được
đánh dấu đã nghe xác minh bằng tai**. Kết quả nhận dạng có thể bỏ lời, nhận
sai hoặc sinh lời không có trong âm thanh.

## Các câu đã sửa trong bảng TTS của game

| Khóa tệp | Lời Anh làm căn cứ | Sửa bản Việt |
|---|---|---|
| `bastard_gameover_f` | I can make a zombie out of you. | Khôi phục ý **biến ngươi thành zombie**, thay vì chỉ tận dụng xác. Turbo nhận rõ; small.en nhận sai thành “his hobby”. |
| `bastard_urban_10_2` | Music, Maestro! | **Nhạc trưởng, nổi nhạc lên!**, thay vì “giai điệu quái vật”. Hai mô hình nhận đúng lời gọi nhạc trưởng. |
| `bastard_maya_9_1` | You have a banjo! | **Đừng lo, ngươi đã có cây đàn banjo rồi!**, thay cho câu hỏi “ngươi có cây đàn banjo không?”. |
| `bastard_tutorial_5_1` | I'll tell you what they will do. | **Ta nói cho ngươi biết chúng sẽ làm gì**, thay cho chỉ nói “ta biết”. |
| `bastard_zombie_berserk_a` | Stay still, and it will go away. | Nói rõ **hãy đứng yên**, thay cho “cứ để yên” còn mơ hồ về hành động của người chơi. |
| `bastard_zombie_clown_a` | Amuse my crowd, and be amused by the clown! | Bổ sung ý **hãy làm khán giả của ta vui** vào câu kết, trước đây bị lược mất. |
| `bastard_tutorial_1_6` | I would pat you on the back, but… | **Ta muốn vỗ lưng chúc mừng ngươi, nhưng…**, thay cho phủ định thẳng. Hai lượt turbo có/không bộ lọc lời nói nhận cùng ý; small.en nhận sai “would”. |
| `bastard_tutorial_10_4` | my infamous zombie arena | **đấu trường zombie khét tiếng của ta**, thay cho “đấu trường zombie riêng”. |

Các câu trên đã được sửa trực tiếp trong
`audiodefence/game/voice_drafts_vi.py`. TTS dùng lại bảng này khi phát tệp
gốc, không cần nhận dạng giọng nói trong lúc chơi.

## Phần chưa thể xác nhận lời thoại

| Tệp | Kết quả đối chiếu | Xử lý hiện tại |
|---|---|---|
| `bastard_gameover_j` — 2,810 giây | Turbo nhận “I'm only a god”; small.en nhận “Than only a god”; medium.en nhận “That's all you got!”. Nhận dạng riêng hai kênh vẫn không khớp. | Giữ câu cũ **“Thế là xong! Bùm!”** nhưng đánh dấu chưa có căn cứ xác nhận phần đầu. |
| `revive_yes` — 2,322 giây | Có lượt không nhận được lời; có lượt sinh câu khác hoặc lặp chữ E vô nghĩa. | Câu cũ **“Audio Defence!”** chưa được xác nhận. Không lấy vòng lặp ASR làm lời dịch mới. |
| `revive_no` — 4,063 giây | Kết quả rỗng, “you” hoặc “Thank you”. Một lượt sinh timestamp tới 29,98 giây, vượt độ dài tệp. | Câu cũ **“Hết rồi!”** chưa được xác nhận. |
| `revive_standby` — 8,057 giây; nằm ngoài 114 bản dịch | Hai lượt đầy đủ trả rỗng; các lượt khác sinh “You” hoặc “Thank you” với thời gian không hợp lý. | Vẫn chưa gán lời Việt; chưa thể kết luận có lời nói hay chỉ hiệu ứng. |

Ba câu cũ ở trên vẫn còn trong bảng TTS; **chúng không phải kết quả dịch
mới đã được duyệt**. Không tự bỏ tiếng nói hoặc bịa câu chỉ vì ASR thất bại.
19 âm mẫu Zombiepedia vẫn thuộc nhóm cần phân loại riêng của lần kiểm kê
ban đầu, không nằm trong 114 bản dịch của đợt đối chiếu này.

## Những lỗi của ASR đã được tránh

- Bộ lọc lời nói của turbo bỏ cả hai đoạn mở đầu Dr. Bastard. `small.en`
  và turbo không bộ lọc đều nhận **“And here we go!”**, phù hợp câu Việt.
- Câu hỏi “Where are the clowns?” được hai lượt không bộ lọc nhận đúng,
  trong khi lượt turbo có bộ lọc nhận thành “Oh, the clown”. Giữ bản Việt
  “Lũ hề đâu hết rồi?”.
- Không chép chuỗi tiếng cười lặp quá mức vào TTS. Không đổi cảm thán ở
  đoạn kết thành phố thành tên nhân vật mà lượt ASR có prompt nhận sai.
- Log probability và no-speech probability được lưu để xem xét, không
  diễn giải chúng thành tỷ lệ bản dịch đúng hoặc bằng chứng không có lời nói.

## Dữ liệu từng câu và cách chạy lại

`analysis/voice_asr_review_20261008.json` chứa **đủ 114 khóa**, đường dẫn
audio, SHA-256, bản Việt trước/sau, lời Anh từ từng lượt, lý do giữ/sửa và
trạng thái còn mơ hồ. `revive_standby` nằm riêng ở mục `unmapped`.
Bản dễ đọc gồm đủ 114 câu Anh–Việt, trạng thái và tệp gốc nằm ở
`docs/VOICE_TRANSLATIONS_VI_114_20261008.md`.

Các tệp chứng cứ giữ nguyên segment và timestamp:

- `analysis/voice_asr_turbo_20261008.json`: 115 tệp, turbo có VAD và prompt tên riêng.
- `analysis/voice_asr_small_20261008.json`: 115 tệp, small.en không VAD và không prompt.
- `analysis/voice_asr_targeted_20261008.json`: 9 tệp, turbo không VAD/prompt.
- `analysis/voice_asr_ambiguous_medium_20261008.json`: 4 tệp, medium.en không VAD/prompt.
- `analysis/voice_asr_gameover_left_20261008.json` và
  `analysis/voice_asr_gameover_right_20261008.json`: nhận dạng riêng kênh trái/phải của câu thua còn mơ hồ.

Phiên bản model được ghi trong báo cáo JSON. Dùng `faster-whisper 1.2.1`,
`CTranslate2 4.8.2`, CPU int8, beam 5, temperature 0, không dùng nội dung
segment trước để dẫn dắt segment sau. Âm thanh được giải mã bằng ffmpeg
thành mono 16 kHz float32, trừ hai lượt chỉ định kênh.

Công cụ chạy lại không sửa bảng Việt và không tự duyệt lời thoại:

```sh
python -m pip install faster-whisper==1.2.1
python tools/recheck_voice_asr.py --model small.en --output analysis/recheck_small.json
python tools/recheck_voice_asr.py --model large-v3-turbo --output analysis/recheck_uncertain.json --keys bastard_gameover_j revive_yes revive_no revive_standby
```

Cần có ffmpeg. Model được tải nếu chưa có trong bộ nhớ đệm; có thể truyền
`--model` đường dẫn model đã tải và `--cache` thư mục cache. Chạy lại có thể
cho kết quả khác giữa phiên bản thư viện/model; file chứng cứ đã lưu giữ
đúng kết quả của đợt này.

## Kiểm tra sau khi sửa

- 23/23 bài kiểm thử tiếng Việt/TTS đạt, gồm cả luồng gọi companion trên desktop.
- 1.520/1.520 mục dịch không rỗng; 1.067/1.067 câu mã nguồn được bộ trích xuất nhận diện có bản dịch.
- 1.655 chuỗi Việt đã kiểm tra; không phát hiện mệnh đề Anh bị kẹp theo quy tắc hiện có.
- Đủ 114 bản đối chiếu; SHA-256 của audio và bản Việt hiện tại khớp dữ liệu báo cáo.

Các thay đổi đang ở bản mã nguồn cục bộ, chưa đẩy lên GitHub hoặc tạo APK
mới. Chưa kiểm tra phát giọng trên điện thoại, Windows hay macOS thật.
