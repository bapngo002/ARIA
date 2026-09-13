# ARIA concept 1 — bản nháp mô hình 3D

Đây là mô hình 3D có thể xoay và chỉnh sửa, phái sinh từ mẫu pixiv. **Chưa tái tạo được diện mạo và độ chân thực của ảnh concept 1.** Không phải mô hình dựng lại tự động từ một ảnh, chưa được chủ dự án duyệt thay nhân vật trong app.

## Các file

- `aria-concept-01-draft.blend`: nguồn Blender 5.2, textures đóng gói, bộ xương, shape keys và cảnh chiếu sáng để chỉnh sửa.
- `aria-concept-01-draft.glb`: bản glTF 2.0 nhúng textures để xem bằng trình duyệt. Hai clip Root và Face cần phát cùng nhau để có cả chuyển động đầu và biểu cảm.
- `front.png`, `three-quarter.png`: ảnh render từ mô hình thật bằng Blender; không phải ảnh concept.
- `build-report.json`: số lượng đỉnh/xương/shape keys và phiên bản công cụ.
- `source-license-settings.json`: điều kiện sử dụng gốc đi kèm mô hình.

Mở app local rồi truy cập `/model-preview` để xoay/thu phóng và bật/tắt chuyển động. Trang chính vẫn dùng nhân vật trước đó. Bản GLB cần thư mục assets của repo; nếu chỉ chép software/pi thì route mô hình trả 404.

## Nguồn và thay đổi

Nguồn: [VRM1_Constraint_Twist_Sample v1.0.1](https://github.com/pixiv/three-vrm/blob/v3.4.2/packages/three-vrm/examples/models/VRM1_Constraint_Twist_Sample.vrm), (c) 2022 pixiv Inc.

Giấy phép: [VRM Public License 1.0](https://vrm.dev/licenses/1.0/) cùng điều kiện trong `source-license-settings.json`, **không phải CC0**. Cho phép sửa đổi/phân phối bản sửa và sử dụng thương mại; cấm sử dụng antisocial/hate theo điều kiện gốc. Không có sự bảo trợ của pixiv.

Thay đổi: điều chỉnh thể tích má/cằm/mũi, giảm tỷ lệ mắt anime, thêm thể tích môi và sắc độ vùng má/môi/hốc mắt; tóc tối màu có biến dạng nhẹ và các sợi hình học mảnh bám bề mặt, vật liệu da/mắt/tóc, áo indigo và cổ áo có viền; thêm hoạt cảnh quay đầu, chớp mắt và miệng. Lớp màu da được chọn làm COLOR_0 trong GLB để trình duyệt hiển thị đúng. Giữ nguyên nguồn VRM trong software/pi/app_ui/models. Mesh, textures và bộ xương nền là tài sản phái sinh pixiv, không nhận là nhân vật gốc tự dựng hoàn toàn.

Tái tạo từ gốc bằng Blender: chạy `tools/avatar/build_concept_01.py` từ repo với Blender ở chế độ background, `--factory-startup --python-exit-code 1 --python`. Script sẽ tạo lại các file tại thư mục này; hãy lưu bản chỉnh sửa thủ công sang tên riêng trước khi chạy lại.

## Kiểm chứng và giới hạn

- VERIFIED: Blender xuất nguồn và GLB; 48.103 đỉnh, 154 xương, 57 shape keys khuôn mặt; render hai góc nhìn. GLB mở và render trong trình duyệt PC; nút góc nghiêng và màu da/môi đã kiểm tra trực quan.
- PARTIALLY VERIFIED: hoạt cảnh mẫu 6 giây dùng bộ xương/shape keys đã xuất. Chưa kiểm tra toàn bộ 57 biểu cảm riêng lẻ. Thân giữ T-pose; chưa có rig tóc vật lý hoặc diễn xuất toàn thân đã kiểm chứng.
- NOT VERIFIED: giống ảnh concept 1, chất lượng hoạt hình 3D chân thực, duyệt ngoại hình, hiệu năng Pi, đồng bộ giọng nói và tích hợp UI chính.

GLB dùng vật liệu PBR; ánh sáng và tán xạ da có thể khác cảnh Blender. GLB không mang bộ điều khiển VRM gốc nên không thay trực tiếp file VRM trong loader hiện tại. Mẫu vẫn mang cấu trúc anime; sợi bổ sung chỉ tăng chi tiết bề mặt, không phải tóc được mô phỏng vật lý. Bước tiếp theo để tiến đến chất lượng ảnh concept là dựng lại hình học mí mắt/mũi/môi và các lọn tóc, rồi kiểm rig/biểu cảm; chưa coi tinh chỉnh vật liệu là đạt độ chân thực. Bản đầu có thể khôi phục nguyên vẹn từ commit ccef30b.
