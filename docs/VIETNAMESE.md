# AudioDefence tiếng Việt

Tài liệu dành cho bản Việt hóa của `tvhuy99-web/1234huyhuy`.
Bản dịch đang được thực hiện trên nhánh `feat/vietnamese-localization`, **chưa phải bản APK hoàn chỉnh**.

## Trạng thái

- Bản dịch: `localization/Tiếng Việt.json`. Tệp có cùng 1.495 khóa với `localization/ru.json`.
- Đã hoàn thành **bản dịch vòng đầu của 1.495/1.495 câu/mục tham chiếu (100%)**. Đây là mức bao phủ của tệp `ru.json`, **chưa xác nhận rằng bộ trích xuất mã nguồn không phát sinh câu mới**.
- Quy tắc số nhiều: `"@plural": "none"`. Tiếng Việt không cần những dạng số nhiều như tiếng Anh hoặc tiếng Nga.
- Trên Android, chọn **Tiếng Việt** sẽ yêu cầu cả giọng TTS thứ nhất và thứ hai dùng `vi-VN`. Nếu máy thiếu giọng Việt, bộ máy đọc quay về ngôn ngữ điện thoại, rồi tiếng Anh nếu cần.
- Giọng người thông báo và các hội thoại thu âm của game **vẫn bằng tiếng Anh**. Bản dịch JSON chỉ xử lý câu chữ.
- Cơ chế kiểm tra cập nhật trong bản fork dùng release của `tvhuy99-web/1234huyhuy`, không cài nhầm phiên bản gốc. Khi fork chưa phát hành bản mới, sẽ không có APK nào để tự cập nhật.

## Cách bật tiếng Việt

1. Cài bản APK được **biên dịch từ nhánh Việt hóa**. APK ở repository gốc không chứa bản dịch này.
2. Mở game, sử dụng tai nghe stereo.
3. Vào **Settings → Miscellaneous → Language → Tiếng Việt**.
4. Nếu giọng nói phát âm tiếng Việt chưa đúng, hãy kiểm tra bộ máy chuyển văn bản thành giọng nói trên Android và cài dữ liệu giọng Việt, nếu được hỗ trợ.
5. Khi chơi, tắt TalkBack theo hướng dẫn của game. Nếu mở trình chọn tệp hệ thống để sao lưu/nhập dữ liệu, hãy bật TalkBack khi thao tác ở màn hình Android đó và tắt lại trước khi chơi.

Lưu ý: một số câu của Java được đọc lúc khởi động **trước khi mã Python nạp ngôn ngữ đã lưu** có thể vẫn bằng tiếng Anh. Đây là một hạng mục phải hoàn thiện khi kiểm thử Android.

## Nguyên tắc biên dịch nội dung

- Dịch tự nhiên, ngắn gọn, dễ hiểu khi **nghe**, không dịch máy từng chữ.
- Thuật ngữ thống nhất: `Challenge` → **Thử thách**; `Endless` → **Vô tận**; `Armory` → **Kho vũ khí**; `Loadout` → **Trang bị**; `Reload` → **Nạp đạn**; `Coins` → **xu**; `Diamonds` → **kim cương**; `Power-up` → **vật phẩm hỗ trợ**.
- Giữ nguyên tên gốc nếu việc dịch có thể khiến người chơi nhầm âm thanh, đặc biệt là tên riêng, tên nhân vật và các mã nội bộ.
- Không làm thay đổi khóa tiếng Anh bên trái dấu hai chấm trong JSON. Chỉ điền phần giá trị tiếng Việt.
- Bảo toàn chính xác `%i`, `%d`, `%s`, `%.1f`, `%%` và các tham số định dạng khác. Với chỗ đổi thứ tự hai tham số, chỉ dùng cú pháp có đánh số theo hướng dẫn README.
- Trong tệp JSON dùng **Nhấn Enter**, **Shift cộng Enter** và **Escape** cho bàn phím máy tính. Trên điện thoại, `speech_android.phone_words` chuyển hướng dẫn thành **chạm đúp**, **chạm đúp và giữ** và **vuốt qua lại bằng hai ngón** khi phát. Cách này giúp một tệp dịch dùng được ở cả Android và Windows.
- Các hướng dẫn trong trận cần tránh dài dòng để không che tiếng bước chân và tiếng định hướng zombie.

## Công việc còn lại trước khi phát hành

1. Chạy bộ trích xuất `tools/make_language.py` trên môi trường có đầy đủ nguồn game để phát hiện câu mới ngoài 1.495 mục tham chiếu; dịch ngay những mục đó.
2. Chạy trình kiểm tra bằng Python, xác minh tính đầy đủ, tham số và ngữ pháp số nhiều. Hiện mới xác minh **tĩnh trên dữ liệu GitHub**, chưa thực thi lệnh trên môi trường build thực tế.
3. Nhờ người chơi nghe thử toàn bộ hướng dẫn, thông báo chiến đấu và các đoạn văn dài. Chỉnh những câu quá dài hoặc khó hiểu khi đọc TTS.
4. Kiểm thử cả hai giọng TTS tiếng Việt trên điện thoại, kể cả thay đổi ngôn ngữ trong lúc game đang chạy và khi thiết bị thiếu giọng Việt.
5. Rà soát lời thoại thu âm tiếng Anh; nếu bổ sung lời dẫn TTS tiếng Việt thì phải kiểm tra không phát đè tiếng zombie, không làm trễ đợt tấn công.
6. Build APK và kiểm thử Challenge, Endless, Extra, cập nhật và sao lưu trên Android thực tế.

## Kiểm tra bản dịch

Từ thư mục gốc của repository:

```powershell
py tools/make_language.py "Tiếng Việt"
py tools/check_vietnamese.py
py tools/verify_localization.py --language "Tiếng Việt"
```

Lệnh đầu bổ sung câu mới còn thiếu trong bộ dịch nếu mã nguồn đã phát triển. Lệnh `check_vietnamese.py` phát hiện thiếu dịch và lỗi tham số đối chiếu với `ru.json`. Lệnh `verify_localization.py` kiểm tra trực tiếp cả mã game và dữ liệu màn chơi; nó có thể tìm thêm các câu chưa có trong tệp tham chiếu.

Khi sẵn sàng phát hành, chạy:

```powershell
py tools/check_vietnamese.py --strict
py tools/verify_localization.py --language "Tiếng Việt"
```

**Các kiểm tra này chưa được thực thi trong môi trường build ở giai đoạn hiện tại.** Cả hai phải đạt sau khi chạy công cụ trích xuất và trước khi phát hành.

## Kiểm tra chất lượng Android

- Cài mới: các bước nạp dữ liệu, giọng đọc, hướng dẫn ban đầu hoạt động.
- Chuyển English → Tiếng Việt → English: menu đổi ngay, cả hai giọng TTS đổi đúng, không cần khởi động lại.
- Cảm ứng: vuốt giữa các mục, chạm đúp, chạm đúp và giữ, cử chỉ quay về, điều khiển trong Gesture và Button.
- Speech: thử cả giọng thứ nhất và thứ hai, bộ TTS có và không có dữ liệu tiếng Việt; xác nhận fallback không gây im lặng.
- Challenge: ít nhất năm bài hướng dẫn; nghe rõ hướng, bắn, đổi súng, nạp đạn, tiếng tim đập, thông báo kết quả.
- Endless: Tarot, trang bị, kiếm xu và kim cương, hồi sinh, vật phẩm hỗ trợ.
- Extra: mục tiêu thử thách, lời dẫn bằng văn bản và lời thoại thu âm tiếng Anh được phân biệt rõ.
- Nhập/xuất sao lưu; cài đặt, kiểm tra cập nhật và phục hồi sau khi đóng game.
- So sánh Windows: các hướng dẫn bàn phím vẫn dùng `Enter` và `Escape` chính xác.
- Xác nhận không có mất âm thanh 3D, tiếng zombie, tiếng súng, hiệu ứng HRTF hoặc trễ tiếng trong giao tranh đông.

## APK thử nghiệm qua GitHub Actions

Nhánh Việt hóa có quy trình tự động:
[Kiểm thử bản dịch](../.github/workflows/vietnamese.yml) và
[Biên dịch APK Android](../.github/workflows/android-vietnamese-debug.yml).

Để nhận APK **khi quy trình Android báo thành công**:

1. Mở mục **Actions** của repository trên GitHub.
2. Chọn **Vietnamese Android debug APK**, rồi chọn lần chạy có dấu thành công.
3. Cuộn xuống **Artifacts**, mở `AudioDefence-Vietnamese-Android-DEBUG`.
4. Giải nén tệp ZIP được GitHub tải về; tệp `.apk` nằm bên trong.

Bản này được Gradle ký bằng **khóa debug tự sinh của máy build**, chỉ dành cho thử nghiệm.
Nó không dùng khóa của APK gốc, không phải bản phát hành và không bảo đảm cập nhật đè
lên APK thử nghiệm trước đó (khóa debug trên các runner có thể khác nhau).

**Bảo vệ dữ liệu chơi:** trước khi gỡ bản gốc để cài APK debug, hãy dùng
**Settings → Miscellaneous → Export backup**. Giữ một bản sao ở nơi an toàn,
vì Android có thể từ chối cài đè ứng dụng có chữ ký khác. Khi nhập dữ liệu,
hãy đọc kỹ thông báo khôi phục trước khi xác nhận.

Chỉ báo APK đã sẵn sàng khi toàn bộ các bước **Build**, **Verify Vietnamese assets**
và **Upload artifact** đều thành công. Nếu workflow thất bại, chưa có APK hợp lệ.

## Biên dịch APK

Làm theo mục [Hướng dẫn build APK Android trong README](../README.md#building-the-app-1). Trên Windows,
dùng Python 3.13, Java 21, Android SDK và Gradle được nêu ở đó.

```powershell
py tools\android_setup.py
py tools\android_keys.py
py compiler.py --android
```

**Quan trọng về dữ liệu và chữ ký:** APK tự build dùng khóa ký khác APK của tác giả gốc, nên thường **không cài đè được**. Hãy dùng **Export backup** trước khi gỡ bản cũ. Giữ khóa ký bản fork an toàn ở máy build; không đưa lên GitHub. Bản cập nhật do fork phát hành sau này phải dùng cùng khóa thì Android mới cài đè được.

Không tuyên bố APK đã được thử nghiệm cho đến khi có thiết bị Android thật thực hiện các bước kiểm tra ở trên.
