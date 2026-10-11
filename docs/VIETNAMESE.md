# AudioDefence tiếng Việt

Tài liệu dành cho bản Việt hóa của `tvhuy99-web/1234huyhuy`.
Bản dịch đang được thực hiện trên nhánh `feat/vietnamese-localization`, **chưa phải bản APK hoàn chỉnh**.

## Trạng thái

- Bản dịch: `localization/Tiếng Việt.json`, có **1.520 khóa** (1.495 khóa tham chiếu cộng 25 câu bổ sung tìm thấy qua rà soát).
- **Kiểm tra nguồn: 1.067/1.067 câu phát sinh từ mã và dữ liệu có bản dịch**, và kiểm tra 1.520/1.520 mục JSON thành công. Đây là kiểm tra tĩnh, không thay thế thử nghiệm TTS trên thiết bị thật hoặc đối chiếu lời thoại thu âm.
- Quy tắc số nhiều: `"@plural": "none"`. Tiếng Việt không cần những dạng số nhiều như tiếng Anh hoặc tiếng Nga.
- Trên Android, chọn **Tiếng Việt** sẽ yêu cầu cả giọng TTS thứ nhất và thứ hai dùng `vi-VN`. Nếu máy thiếu giọng Việt, bộ máy đọc quay về ngôn ngữ điện thoại, rồi tiếng Anh nếu cần.
- Các tệp thoại gốc vẫn là tiếng Anh; cơ chế TTS tiếng Việt đọc đi kèm đã bao phủ đa số tệp thoại ở mức bản nháp, chưa được duyệt từng bản chép lời. Xem mục **Đọc tiếng Việt đồng thời với lời thoại gốc**.
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

## Đọc tiếng Việt đồng thời với lời thoại gốc

Khi người chơi chọn **Tiếng Việt**, game phát câu TTS cùng lúc với bản ghi
âm tiếng Anh được định danh trên Android, Windows và macOS. Android yêu cầu
giọng `vi-VN`; desktop dùng giọng đã chọn trong game/trình đọc màn hình và
cần có giọng tiếng Việt được cài đặt để phát âm đúng. Chỉ giảm âm
lượng **tệp giọng người nói gốc** còn khoảng 32%; **tiếng zombie, bước chân,
tiếng súng, vật cản và âm thanh HRTF không bị giảm**.

**Phạm vi bản nháp:** **88/88 lời thoại Challenge** đã có bản dịch từ bản
chép lời tiếng Anh bằng nhận dạng giọng nói. Các nhóm khác có thêm 21 nhãn
vũ khí/thông báo ngắn, 13 hướng dẫn dùng điều khiển, 15 câu khi thua, 4 giọng
trong mở đầu, cùng các câu hồi sinh và hướng dẫn bổ sung. Tổng cộng có
**114 lời dịch từ ASR** trong `audiodefence/game/voice_drafts_vi.py`.
Toàn bộ 114 đoạn đã được nhận dạng lại bằng hai mô hình và so với bản Việt
ngày 08/10/2026; các lỗi tìm thấy đã được sửa. Xem
[báo cáo ASR](VOICE_ASR_REVIEW_20261008.md) để biết từng câu sửa và những
đoạn còn mơ hồ. Đây là đối chiếu văn bản tự động, **chưa phải nghe xác minh
bằng tai** hoặc kiểm thử bản dịch hoàn chỉnh trên thiết bị.

- Mã `ADSound` đọc lời Việt theo từng tệp Challenge và kéo dài thời gian
  chặn đợt zombie khi TTS tiếng Việt dài hơn bản thu. **Bỏ qua** dừng TTS;
  **tạm dừng/tiếp tục** đọc lại từ đầu, vì Android TTS không thể dừng giữa câu.
- Các thông báo ngắn, phần mở đầu, thua trận và hồi sinh dùng điểm phát
  `S3DSound.play`. Trình phát ngăn câu TTS trùng, khôi phục âm lượng bản thu
  khi kết thúc và không ghi đè callback điều khiển diễn biến game.
- Tutorial tiếp tục dùng `game/tutorial_text.py` để nhắc đúng thao tác
  trên điện thoại. Không phát trùng cùng câu ở hai cơ chế.
- `revive_standby` chưa có lời TTS vì nhận dạng giọng nói trả ra những
  câu mâu thuẫn, chưa xác định đó có phải lời nói có nghĩa không.
- 19 tệp nghe thử ở Zombiepedia là **âm thanh của zombie** theo mã nút
  `Preview sound`; chúng được giữ nguyên, không phải lời thoại để dịch.
- Xem bảng đầy đủ ở `analysis/voice_inventory.json` và tiêu chuẩn nghiệm
  thu tại [VOICEOVER_COVERAGE.md](VOICEOVER_COVERAGE.md).

**Để đạt 100% đã xác minh**, cần nghe sửa từng bản chép lời Anh, rà soát ý
nghĩa câu Việt, thử Android thật với giọng `vi-VN`, và kiểm tra tiếng
trong trận không che âm thanh định hướng.

## Công việc còn lại trước khi phát hành

1. Bộ trích xuất và kiểm thử CI hiện có 1.520 mục, trong đó có 25 câu nằm ngoài danh mục Nga cũ. Cần tiếp tục chạy chúng và rà soát các chuỗi ghép động khi mã game thay đổi.
2. Bộ kiểm tra Python và bản dịch đã chạy thành công trên GitHub Actions. Tiếp tục chạy lại mỗi khi chỉnh mã TTS, theo dõi các câu mới và xử lý lỗi CI phát sinh.
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
