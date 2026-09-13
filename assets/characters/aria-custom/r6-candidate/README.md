# ARIA R6 — bản thử khuôn mặt có chuyển động

Đây là mesh 3D thật phát triển từ đầu R4 đã có, không phải mô hình tái dựng chính xác từ ảnh. Ảnh ba góc được giữ trong file Blender để đối chiếu. R4 vẫn là bản đã chọn; R6 là ứng viên mới, chưa được người dùng duyệt.

## Mở và thử

- Mở `aria-face-r6.blend` bằng Blender; nhấn Space để xem đoạn thử 4 giây.
- Chọn `ARIA_R6_Head`, mở Object Data Properties → Shape Keys để thử các giá trị 0–1. Animation hiện có sẽ ghi đè giá trị khi đổi frame; dùng bản sao file khi chỉnh.
- GLB và FBX là bản xuất để thử trong trình xem/ứng dụng khác; chưa thay avatar đang chạy của ARIA.
- Các key cùng tên cũng nằm trên mắt, răng, lưỡi và lông mày/mi. Khi điều khiển bằng code, cần cập nhật key đó trên TẤT CẢ mesh có key tương ứng. `tongueOut` chỉ có dịch chuyển đáng kể trên lưỡi, không trên da mặt.

## Có gì trong bản này

- Đầu/cổ dạng quad từ MPFB, giữ tỷ lệ mặt R4; đã làm mượt một cấp cho bản xuất.
- Mắt riêng, răng, lưỡi, hình học miệng; bộ xương MakeHuman có xương đầu và cổ (còn các xương toàn thân chưa tối ưu).
- 52 shape keys ARKit-style lấy từ MakeHuman faceunits01. Đoạn mẫu: chớp mắt, mở miệng, cười, nhìn ngang và xoay đầu. Không phải lip-sync với audio.
- Tóc dài dạng khối mesh và màu da/cổ áo sơ bộ. Tóc chưa đạt kiểu tóc/độ tự nhiên của ảnh; chưa có texture da chi tiết.

## Kiểm chứng và giới hạn

`build-report.json` ghi số đỉnh/mặt/xương. `export-validation.json` ghi kết quả nhập lại GLB và FBX, kiểm 52 tên key, dịch chuyển hình học trên các mesh và animation GLB sau khi nhập lại. Các kiểm tra này chứng minh dữ liệu tồn tại và chạy, không chứng minh mọi biểu cảm đẹp hay mọi tổ hợp không xuyên nhau.

Đã xem render chính diện, góc 3/4, nghiêng, chớp mắt và mở miệng. Độ giống ảnh chưa đạt; tóc còn cứng, mí và miệng cần chỉnh corrective shapes. Vùng răng/lợi đã lùi để hạn chế xuyên môi khi mở hàm; chưa kiểm hết mức 0–1 và mọi tổ hợp. Cần kiểm soát tiếp mắt/mi, răng/lợi, má và môi trước bản dùng thật.

Chưa kiểm trên Raspberry Pi, chưa nối voice/audio, chưa đổi pipeline ARIA. Không có thao tác phần cứng. Kích thước file và độ phức tạp hiện tại dành cho thử trên PC, chưa tối ưu cho Pi.

## Nguồn và tái tạo

- Blender 5.2 và MPFB 2.0.17 có sẵn trong hồ sơ ARIA; source base được giữ ở R4.
- Faceunits: https://github.com/makehumancommunity/extra-targets — commit `7eaba3453134385bb5ea9811ef0b33b85b4b556d`, CC0, bộ tự sinh do Mika Suominen đóng góp.
- Răng `teeth_base`, lưỡi `tongue01`: https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html — CC0; giữ license đính kèm.
- Ảnh tham chiếu: ảnh người dùng đã cung cấp trong “Tạo mô hình 3D”; không gán giấy phép CC0 cho ảnh này.
- Builder: `tools/avatar/build_face_r6.py`; validator: `tools/avatar/validate_face_r6.py`. Builder tạo lại ứng viên và ghi đè file R6, nên lưu riêng mọi chỉnh tay trước khi chạy. Cần profile MPFB tại `D:/UserData/ARIA/tools/blender-profile`, extra-targets và teeth/tongue tại thư mục tools hiện có. File Blender đã đóng gói ảnh cần thiết để mở độc lập.

Bước tiếp: chỉnh silhouette tóc, đường chân tóc và khuôn mặt theo ảnh trước; sau đó chỉnh biểu cảm theo từng key và tổ hợp. Chỉ tích hợp sau khi duyệt ngoại hình và đo hiệu năng trên thiết bị.
