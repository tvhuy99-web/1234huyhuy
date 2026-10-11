# Cài cập nhật AudioDefence Android bằng chữ ký cố định

Kể từ phiên bản `26.10.11-1`, bản **Debug** của AudioDefence được ký
bằng **cùng một khóa kiểm thử công khai** lưu tại
[`.github/signing/stable-debug.keystore.b64`](../.github/signing/stable-debug.keystore.b64).
Cách làm được tham khảo từ kho GeminiLiveTranslate của cùng chủ sở hữu.

## Khi nào Android cho cài đè?

APK mới phải có cùng cả ba yếu tố:

1. Tên gói: `com.audiodefence.android` (giữ nguyên).
2. Chữ ký số: cùng chứng chỉ từ file `stable-debug.keystore.b64`.
3. `versionCode`: không được thấp hơn bản đã cài. Với mỗi bản cập nhật mới,
   nâng file [`VERSION`](../VERSION) lên phiên bản lớn hơn
   (ví dụ `26.10.11-1` → `26.10.12-1`). Không chỉ đổi tên file APK.

Mỗi lần build `gradle -p android :app:assembleDebug` hay GitHub Actions
`Vietnamese Android debug APK`, Gradle tự giải mã đúng khóa vào
`android/.gradle/stable-debug.p12` (nơi bị Git bỏ qua).
Không phụ thuộc khóa Debug ngẫu nhiên của máy chạy GitHub.
Workflow kiểm tra vân tay **trước và sau** khi ký, và tự build lại sau
khi push thay đổi lên `master`.

## Chữ ký đã chốt, không thay đổi

- **SHA-256:** `FE:16:06:AE:04:59:E6:82:3E:54:9A:4F:50:40:4B:59:E2:63:19:8D:DA:30:B3:3E:CC:1A:7F:3D:4B:E9:ED:5D`
- Alias: `audiodefence-stable-debug`.
- Mật khẩu keystore/key: `android` (chỉ dành cho thử nghiệm).

**Không tạo lại hoặc thay khóa** nếu muốn cài cập nhật từ bản này về sau.

## Lần chuyển đổi đầu tiên

Các APK Debug cũ, kể cả bản ngày 11/10/2026 trước khi thiết lập chữ ký,
được GitHub ký bằng khóa ngẫu nhiên khác nhau. **Không thể cài đè** APK
dùng chứng chỉ mới lên các APK đó; không thể suy ra khóa cũ từ file APK.

1. Trong game cũ, mở **Settings → Miscellaneous → Export backup** và lưu
   tệp sao lưu ngoài điện thoại hoặc ít nhất ngoài vùng dữ liệu ứng dụng.
2. Gỡ ứng dụng cũ, nếu Android báo chữ ký khác. Việc gỡ có thể xóa dữ liệu
   trong ứng dụng.
3. Cài APK mới mang chữ ký cố định.
4. Dùng **Import backup** trong game để khôi phục.
5. Từ lần sau, giữ nguyên khóa ký và tăng `VERSION` thì có thể cài đè
   các APK phát hành từ cùng nhánh, không cần gỡ nữa.

## Giới hạn an toàn

Khóa này được cố ý **công khai** để dự án mã nguồn mở dễ build. Do đó
**bất kỳ ai cũng có thể dùng nó ký APK khác với cùng tên gói**. Chỉ cài
APK từ nguồn GitHub mà bạn tin tưởng và không dùng chứng chỉ công khai
này cho phát hành cần xác thực danh tính nhà phát triển.

Cấu hình ký `release` bằng `AD_KEYSTORE` vẫn **tách biệt** với bản
Debug này. TTS và lối chơi vẫn cần kiểm tra thực tế trên điện thoại.
