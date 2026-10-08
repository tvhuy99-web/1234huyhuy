# Mục tiêu: 100% câu thoại gốc được đọc bằng TTS tiếng Việt

**Không thu âm lại. Không dịch hiệu ứng zombie hoặc âm thanh súng.**
Khi một *đoạn tiếng nói* bắt đầu, TTS đọc câu tiếng Việt tương ứng. Giọng Anh
gốc có thể phát nhỏ ở nền. Không để tiếng nói che âm thanh định hướng.

## Kiểm kê toàn bộ game

Dữ liệu gốc: `analysis/data/sounds.tsv` với 918 tệp âm thanh.
Bảng từng tệp: `analysis/voice_inventory.json`. Tạo lại bằng lệnh:

    python tools/voice_inventory.py --write analysis/voice_inventory.json

| Nhóm | Tệp |
|---|---:|
| Dr. Bastard trong Challenge | 88 |
| Hướng dẫn thu âm | 15 |
| Lời thoại khi game over | 15 |
| Người thông báo (announcer) | 10 |
| Tên vũ khí | 10 |
| Tên vật phẩm hỗ trợ | 4 |
| Lời thoại hồi sinh | 3 |
| Giọng trong đoạn mở đầu | 4 |
| Zombiepedia: âm thanh cần nghe để phân loại | 19 |
| **Tổng cần xem xét** | **168** |

Hiện có 21 tệp nhãn ngắn, 13 tệp tutorial và 11 tệp Challenge được ghép TTS.
**104 tệp chưa có TTS**, **19 tệp Zombiepedia cần phân loại**. Đây là tỷ lệ
bao phủ tệp, **không phải lời cam kết 45 bản dịch đã khớp từng chữ bản thu**.
Các đoạn Challenge đã ghép trước đó chỉ là diễn giải theo ngữ cảnh.

## Quy trình hoàn thiện

1. **Nhận dạng lời nói tiếng Anh.** Workflow `transcribe-voice.yml` dùng
   mô hình Whisper tiếng Anh chạy trên GitHub runner và tạo 2 Artifact:
   `English-voice-DRAFT-challenge` và `English-voice-DRAFT-other`.
   Mỗi mục chứa tên tệp, lời chép tự động, thời gian và thông tin chất lượng.
   Đây là **bản nháp**, không phải lời thoại được xác nhận.
2. **Nghe đối chiếu.** Nghe tệp gốc trong `game/sounds/` và sửa tên riêng,
   con số, câu khó nghe. Với tệp chỉ có hiệu ứng, đánh dấu không phải lời thoại.
   Chỉ duyệt sau khi thực sự nghe.
3. **Dịch tự nhiên.** Dịch chính xác, ngắn gọn, dễ hiểu qua TTS; giữ nguyên
   cảnh báo chiến đấu và hướng dẫn quan trọng. Dùng ánh xạ theo khóa tệp audio
   để game không phải nhận dạng giọng nói thời gian thực.
4. **Kích hoạt TTS ở mọi điểm phát.** Challenge qua `ADSound`; nhãn ngắn qua
   `S3DSound.play`; opener, game over, hồi sinh, Zombiepedia phải được kiểm tra
   riêng. Tránh một tệp phát hai câu TTS.
5. **Đồng bộ.** Bắt đầu khi âm gốc bắt đầu, chỉ hạ riêng tiếng người đang nói.
   Xử lý lời Việt dài hơn bản gốc, skip, pause/resume và giọng thứ hai.
   Giữ nguyên tiếng súng, zombie, bước chân và âm thanh 3D.
6. **Kiểm thử APK thật.** Phát liên tục trong chiến đấu, mở khóa thử thách,
   hồi sinh, đổi vũ khí, cả hai bộ TTS và thiếu giọng vi-VN.

## Khi nào mới được công bố 100%?

Chỉ đánh dấu một tệp thoại là hoàn chỉnh sau khi **đồng thời** xác nhận:
- Đây thực sự là lời nói, không phải âm thanh hiệu ứng.
- Lời chép gốc đã được nghe và xác nhận.
- Câu Việt đã được duyệt về nghĩa, cách phát âm và độ dài.
- TTS thực sự phát đúng lúc trên Android, không bị trùng.
- Skip, pause, resume và âm thanh chiến đấu đều đã kiểm tra.

Dù bảng dịch văn bản đã đủ 1.495 câu, điều đó **không thay thế** kiểm tra
lời thoại ghi âm. Các tệp chưa dịch phải luôn hiện trong bản kiểm kê.

Bản APK hiện tại là debug; hãy xuất sao lưu trước khi gỡ bản cũ.
