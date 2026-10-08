# Báo cáo rà soát cuối: Tiếng Việt và TTS AudioDefence

Ngày kiểm tra: **08/10/2026**. Đối tượng: bản mã nguồn tải từ `master`
của `tvhuy99-web/1234huyhuy` tại commit
`22ff5ac53c069c429ca066842d9adaf88c3a5da1`, cùng các sửa đổi cục bộ.
Các sửa đổi trong lần kiểm tra này chưa được đẩy lên GitHub.

## Kết luận

**Chưa đủ căn cứ xác nhận mọi câu đã được Việt hóa chính xác 100%.**
Độ bao phủ văn bản mã nguồn mà bộ kiểm tra hiện biết đã đạt; còn cần
nghe xác minh lời nói thu âm và chạy thực tế trên thiết bị Android.

| Hạng mục | Kết quả | Độ chắc chắn |
|---|---|---|
| Tệp `localization/Tiếng Việt.json` | **1.520/1.520 giá trị không rỗng** | Kiểm tra tĩnh |
| Câu UI/data được trình quét liệt kê | **1.067/1.067** | Bộ trích xuất mã/game |
| Bài kiểm thử hồi quy | **23/23 đạt** | Chạy cục bộ sau các sửa đổi |
| Challenge, đối chiếu tên audio | **88/88 tệp có câu TTS đi kèm** | Có ánh xạ; bản chép lời chưa duyệt |
| Tổng câu dịch từ ASR gắn audio | **114/114 đã nhận dạng lại và đối chiếu bản Việt** | Hai mô hình ASR; xem báo cáo từng tệp |
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
   tính trong 1.520 mục JSON**, vì chạy trước Python.

Các thay đổi trên có thêm kiểm thử chống tái phát. Trình kiểm tra tĩnh
cũng được mở rộng để đọc bảng hướng dẫn, câu gán `label`/`hint` sau
khi tạo view, lời Ghi công và nguồn giọng hệ thống. Sau khi bổ sung bốn
nhãn điều khiển động còn thiếu, `tools/audit_vietnamese_dynamic.py` vẫn
liệt kê 19 ứng viên: các đoạn con của phần Giới thiệu và Extra đã có bản
dịch cho toàn đoạn, bảy câu tutorial đã có khóa dịch riêng, cùng comment,
chuỗi kiểm thử và quy tắc thay cử chỉ tiếng Anh. Các ứng viên này không
được tính là câu UI còn thiếu; test mới kiểm tra bản dịch phần Giới thiệu,
Extra và nhãn điều khiển.

## Kiểm tra tiếng Anh bị kẹp bên trong câu tiếng Việt

Đã bổ sung `tools/check_vietnamese_embedded_english.py`, gọi bởi workflow
`.github/workflows/vietnamese.yml`. Khác với phép đếm các ô JSON khác
rỗng, công cụ này **kiểm tra bên trong từng câu** của:

- **1.520 giá trị dịch văn bản**.
- **114 câu TTS nháp** được đọc cùng bản ghi âm tiếng Anh.
- **21 thông báo TTS ngắn** cho súng và vật phẩm.

**Kết quả: 1.655/1.655 chuỗi đã quét, 0 cụm tiếng Anh đáng ngờ** theo
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

- **114 câu TTS đã được xử lý và so bản Việt với hai lượt ASR mới**;
  các lỗi tìm thấy đã được sửa. Đây là đối chiếu văn bản từ nhận dạng
  tự động, chưa phải nghe xác minh bằng tai. Các tệp còn mơ hồ và
  toàn bộ lời Anh/Việt được ghi ở `docs/VOICE_ASR_REVIEW_20261008.md`
  và `analysis/voice_asr_review_20261008.json`.
- **`revive_standby.m4a`** chưa thể quyết định là giọng nói hay hiệu ứng.
  Nếu có lời nói thật, vẫn thiếu bản TTS cho tệp đó.
- **19 âm mẫu Zombiepedia** được thiết kế nghe tiếng zombie; cần nghe để
  bảo đảm không chứa câu nói mang nghĩa mà ta chưa phân loại.
- **Windows và macOS hiện cũng gọi TTS kèm các lời thoại đã ánh xạ** qua
  cùng luồng phát giọng của game. Android yêu cầu giọng `vi-VN`; Windows/macOS
  dùng giọng đọc đã chọn trong game hoặc trình đọc màn hình, vì vậy cần cài
  và chọn giọng tiếng Việt trên máy để bảo đảm phát âm tiếng Việt. Chưa có
  kiểm thử thực tế trên Windows/macOS.
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

**Điều kiện ra mắt**: nghe duyệt 114 câu thoại, giải quyết `revive_standby`,
thử APK debug trên thiết bị thật và kiểm tra không có lời tiếng Anh của
người nói bị bỏ qua. Kết quả ASR mới giúp tập trung trước vào các tệp
còn mơ hồ; không thay thế kiểm thử phát giọng thực tế.
