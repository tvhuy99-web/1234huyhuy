# Chữ ký APK cố định để AudioDefence cài cập nhật

## Trạng thái và nguồn tham khảo

Tham khảo cách GitHub CI ký debug APK bằng một chứng thư không thay đổi trong
`tvhuy99-web/GeminiLiveTranslate_GitHubReady_v1.2.`, xem
[UPDATE_SIGNING.md](https://github.com/tvhuy99-web/GeminiLiveTranslate_GitHubReady_v1.2./blob/main/docs/UPDATE_SIGNING.md).
**Khác biệt bảo mật quan trọng:** kho AudioDefence công khai, vì vậy **không**
đưa kho khóa, Base64 của kho khóa hoặc mật khẩu lên Git, kể cả nếu mang tên
"debug". Khóa được lưu an toàn bằng GitHub Actions Secrets.

Bản Android dùng `applicationId=com.audiodefence.android`, không đổi.
Trước đây `assembleDebug` trên GitHub runner tạo chứng thư Debug tạm thời.
Vì mỗi runner có thể có chứng thư riêng, APK mới không chắc cài đè APK cũ.

## Chứng thư cố định

- Tệp riêng tư: `AudioDefence-UpdateSigning-KEEP-PRIVATE.p12`
  (được bàn giao riêng cho chủ kho, **không** đưa vào Git).
- Loại kho khóa: **PKCS12**.
- Alias: **`audiodefence-update`**.
- Chứng thư SHA-256 mong đợi:

```
3a274f80a416c75cac9a2a1c35be1d969ba10fff777dacd570fa8e153ab225fe
```

**Cất một bản sao ngoại tuyến** của tệp `.p12` và mật khẩu ở nơi chỉ bạn truy cập.
Mất khóa là mất khả năng phát hành bản cập nhật tương thích. Không tạo khóa mới
cho mỗi bản build và không dùng khóa công khai từ kho ví dụ.

## Một lần cấu hình GitHub Actions Secrets

Truy cập [Settings → Secrets and variables → Actions](https://github.com/tvhuy99-web/1234huyhuy/settings/secrets/actions).
Trong **Repository secrets**, tạo **hai** mục:

1. `AD_UPDATE_KEYSTORE_BASE64`: Base64 của **toàn bộ nội dung nhị phân**
   tệp `.p12` được bàn giao riêng. Có thể lấy bằng PowerShell:

   ```powershell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\\duong-dan\\AudioDefence-UpdateSigning-KEEP-PRIVATE.p12"))
   ```

   Với macOS/Linux: `base64 < AudioDefence-UpdateSigning-KEEP-PRIVATE.p12 | tr -d '\\n'`.

2. `AD_UPDATE_STORE_PASSWORD`: mật khẩu trong tệp bí mật
   `AudioDefence-UpdateSigning-SECRET-INFO.txt` đã bàn giao riêng.

**Không** đăng nội dung hai mục này lên issue, pull request, file trong kho
hoặc tin nhắn công khai.

## Cơ chế build mới

- Khi workflow `Vietnamese Android debug APK` chạy trên **`master`**
  (push hoặc Run workflow): bắt buộc có **hai Secrets**, giải mã kho khóa
  vào thư mục tạm của runner, ký APK với cùng khóa và so fingerprint thực tế.
  Thiếu Secrets, build **thất bại** thay vì âm thầm ký bằng khóa mới.
- Với **pull request**, chỉ build APK kiểm thử ký bằng khóa tạm thời, tên
  artifact có `PR-TEST-TEMPORARY-SIGNATURE`. **Không cài bản PR này** nếu
  muốn giữ khả năng cập nhật trong tương lai.
- APK từ `master` có artifact `AudioDefence-Android-STABLE-SIGNED`.
  Phải kiểm tra kết quả workflow và chứng thư trước khi phân phối.
- Mã Gradle cũng cho phép ký máy cá nhân: đặt biến môi trường
  `AD_UPDATE_KEYSTORE` là đường dẫn tới tệp `.p12`, và
  `AD_UPDATE_STORE_PASSWORD` là mật khẩu; gọi `assembleDebug`.

## Cập nhật trên điện thoại

Android chỉ cho cài đè khi **cùng applicationId**, **cùng chứng thư ký** và
**versionCode không giảm**. `android/app/build.gradle` đọc
`VERSION` để tạo versionCode dạng `yymmddNN`. Khi phát hành phiên bản
mới hãy **tăng VERSION** (ví dụ `26.10.11-1`, lần sau `26.10.11-2` hoặc
ngày lớn hơn), rồi build từ `master`.

**Chuyển đổi một lần:** APK đã cài từ các runner cũ có khóa ngẫu nhiên
không thể cài đè bằng khóa mới. Khóa riêng không thể được lấy lại chỉ từ APK.
Hãy dùng **Settings → Miscellaneous → Export backup** trong game, cất file
sao lưu, sau đó mới gỡ APK cũ nếu Android báo xung đột chữ ký; cài APK ổn định,
rồi khôi phục bản sao lưu. Từ lần cài bằng chữ ký ổn định trở đi, APK mới
được ký bằng **cùng** khóa có thể cài cập nhật không gỡ ứng dụng.

**Chú ý:** APK Debug không phải bản phát hành production, và workflow chỉ
phát hành artifact; nó chưa tự đăng APK lên GitHub Release. Chức năng kiểm
tra cập nhật trong trò chơi chỉ nhận bản mới trên GitHub Releases với tên
`AudioDefence-Android-<VERSION>.apk`; phải phát hành đúng định dạng để
trình cập nhật trong game nhận ra.
