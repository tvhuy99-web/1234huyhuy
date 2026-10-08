# Báo cáo rà soát cuối: Tiếng Việt và TTS AudioDefence

Ngày kiểm tra: **08/10/2026**. Đối tượng: nhánh
`feat/vietnamese-localization` trong `tvhuy99-web/1234huyhuy`, PR #1 nháp.

## Kết luận

**Chưa đủ căn cứ xác nhận mọi câu đã được Việt hóa chính xác 100%.**
Độ bao phủ văn bản mã nguồn mà bộ kiểm tra hiện biết đã đạt; còn cần
nghe xác minh lời nói thu âm và chạy thực tế trên thiết bị Android.

| Hạng mục | Kết quả | Độ chắc chắn |
|---|---|---|
| Tệp `localization/Tiếng Việt.json` | **1.516/1.516 giá trị không rỗng** | Kiểm tra tĩnh |
| Câu UI/data được trình quét liệt kê | **1.063/1.063** | Bộ trích xuất mã/game |
| Bài kiểm thử hồi quy | **19/19 đạt** | GitHub Actions |
| Challenge, đối chiếu tên audio | **88/88 tệp có câu TTS đi kèm** | Có ánh xạ; bản chép lời chưa duyệt |
| Tổng câu dịch từ ASR gắn audio | **114 câu nháp** | Phải nghe so lại |
| Thông báo ngắn, tên súng/power-up | **21 nhãn TTS** | Theo tên tệp âm thanh |
| Tutorial có văn bản thích ứng điều khiển | **13 tệp** | TTS phát theo cài đặt hướng dẫn |
| Tệp `revive_standby` | **1 chưa xác định** | ASR mâu thuẫn, có thể là nền/hiệu ứng |
| Mẫu âm Zombiepedia | **19 tệp cần kiểm định bằng tai** | Nút Preview sound; không tự đọc mô tả chồng lên âm zombie |

## Những chỗ bộ kiểm tra ban đầu đã bỏ lọt và đã sửa

1. **16 câu hướng dẫn Android/tay cầm** trong các hằng số
   `PHONE_AIM`, `PHONE_LINES`, `PHONE_BUTTON_LINES` và các câu cho joystick.
   Nay các câu như vuốt để đổi súng, nghiêng để ngắm, dùng nút góc màn hình
   đều có mục dịch tiếng Việt.
2. **Màn Ghi công**: dịch tên phần Windows/Mac; tên người và studio vẫn giữ nguyên.
3. **Màn Tarot**: bổ sung lời nhắc giá xáo bài theo kim cương/xu và
   trạng thái xáo miễn phí khi thử nghiệm.
4. **Màn giọng nói Windows/macOS**: bổ sung mô tả nguồn giọng mặc định.
5. **Android hỗn hợp Anh/Việt**: sửa cả hai bộ thay tên phím bằng cử chỉ
   trong `speech_android.py` và `pad.py`, không đọc từ tiếng Anh giữa một
   câu đã Việt hóa.
6. **Android trước khi Python chạy**: bản Java nói thẳng tiếng Anh khi
   chuẩn bị dữ liệu, cập nhật, đọc phần trăm, cảnh báo TalkBack và báo
   lỗi khởi động. `MainActivity.java` đã đọc lựa chọn ngôn ngữ từ
   `AudioDefence/settings.json`, dùng lời Việt khi đã lưu Tiếng Việt;
   lần cài đầu dựa theo ngôn ngữ máy. Đây là nhóm lời thoại **không được
   tính trong 1.516 mục JSON**, vì chạy trước Python.

Các thay đổi trên có thêm kiểm thử chống tái phát. Trình kiểm tra tĩnh
cũng được mở rộng để đọc bảng hướng dẫn, câu gán `label`/`hint` sau
khi tạo view, lời Ghi công và nguồn giọng hệ thống. Các cảnh báo khác
từ `tools/audit_vietnamese_dynamic.py` cần phân loại riêng: nhiều cảnh
báo là phần câu của đoạn Extra **đã dịch nguyên đoạn**, chuỗi regex
hoặc cấu hình nội bộ không đọc cho người chơi.

## Kiểm tra tiếng Anh bị kẹp bên trong câu tiếng Việt

Đã bổ sung `tools/check_vietnamese_embedded_english.py`, gọi bởi workflow
`.github/workflows/vietnamese.yml`. Khác với phép đếm các ô JSON khác
rỗng, công cụ này **kiểm tra bên trong từng câu** của:

- **1.516 giá trị dịch văn bản**.
- **114 câu TTS nháp** được đọc cùng bản ghi âm tiếng Anh.
- **21 thông báo TTS ngắn** cho súng và vật phẩm.

**Kết quả: 1.651/1.651 chuỗi đã quét, 0 cụm tiếng Anh đáng ngờ** theo
hai phép soát tự động:

1. Nhận biết từ ngữ pháp và mệnh lệnh tiếng Anh còn lại trong văn bản
   tiếng Việt, ví dụ `Please try again`, `you have`, `press Enter`,
   `reload your weapon`, kể cả khi trước đó đã có nguyên một câu Việt.
2. Đối chiếu mỗi bản dịch văn bản với **câu tiếng Anh gốc làm khóa** để
   phát hiện **ba từ tiếng Anh liên tiếp còn bị chép nguyên**. Chỉ bỏ
   qua những chuỗi kỹ thuật hoặc tên riêng được phép giữ nguyên như tên
   tác giả, `AudioDefence backup.zip` và đường dẫn trang web.

Kiểm thử tự động cố tình chèn `Zombies attack now` vào câu tiếng Việt
để xác nhận phép soát thứ hai thực sự bắt được lỗi dạng này.
Điều này **không có nghĩa đã kiểm chứng thủ công từng từ**: một hoặc
hai từ tiếng Anh riêng lẻ, lỗi diễn đạt, câu do giá trị biến bên ngoài
đưa vào, hoặc lỗi chép từ âm thanh có thể cần nghe và sửa trực tiếp.

## Những câu được giữ nguyên có chủ ý

Tên riêng `Berserk`, `Hydra`, `Zombie`, phím `Enter`/`Escape`,
từ phổ biến `Menu`, tên người, tên nhà sản xuất và một số mã vũ khí
cần giữ nguyên để không làm mất ý nghĩa và nhất quán với âm gốc.
Đây **không phải** câu văn tiếng Anh bị bỏ quên.

## Những điều chưa kiểm chứng được

- **114 câu TTS ASR chưa được nghe xác minh với bản thu tiếng Anh từng tệp**.
  Có thể sai tên riêng, số, ngắt câu hoặc bỏ sót lời thoại nhỏ dưới
  tiếng hiệu ứng. Bản chép tự động không phải bản dịch chính thức.
- **`revive_standby.m4a`** chưa thể quyết định là giọng nói hay hiệu ứng.
  Nếu có lời nói thật, vẫn thiếu bản TTS cho tệp đó.
- **19 âm mẫu Zombiepedia** được thiết kế nghe tiếng zombie; cần nghe để
  bảo đảm không chứa câu nói mang nghĩa mà ta chưa phân loại.
- **Windows và macOS chưa có TTS đọc kèm lời thoại thu âm**. Bộ ghép
  `ADSound`/`S3DSound.play` đang bật riêng trên Android để dùng giọng
  `vi-VN` của điện thoại. Giao diện Windows/Mac dùng bản dịch chữ,
  nhưng lời ghi âm sẵn vẫn nói tiếng Anh trên các nền tảng đó.
- **Chưa có kiểm thử trực tiếp trên điện thoại Android**. Cần xác nhận
  vi-VN có sẵn, chọn tiếng Việt từ lần chơi trước, tạm dừng, bỏ qua,
  đổi ngôn ngữ, thông báo nối đuôi/đè nhau, tiếng súng/zombie HRTF và
  tiếng giọng thu âm giảm âm lượng. Một thiết bị không có gói giọng
  Việt có thể dùng fallback và phát âm tiếng Việt không chính xác.
- Bộ rà soát tĩnh không thể phát hiện mọi chuỗi được tạo bởi thư viện
  hoặc nhận từ hệ điều hành, dù phần lớn UI game dùng cùng lớp dịch.

## Cách kiểm tra lại

    python tools/check_vietnamese.py --strict
    python tools/verify_localization.py --language "Tiếng Việt"
    python -m unittest discover -s tests -p 'test_vietnamese.py' -v
    python tools/audit_vietnamese_dynamic.py
    python tools/voice_inventory.py

CI kiểm thử ở: https://github.com/tvhuy99-web/1234huyhuy/actions/runs/37722992014

**Điều kiện ra mắt**: nghe duyệt 114 câu thoại, giải quyết `revive_standby`,
thử APK debug trên thiết bị thật và kiểm tra không có lời tiếng Anh của
người nói bị bỏ qua. PR giữ ở chế độ Draft, không merge `master` trước đó.
