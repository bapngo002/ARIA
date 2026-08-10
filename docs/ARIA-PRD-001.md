# ARIA V1 — Product Requirements Document

**Document ID:** ARIA-PRD-001  
**Version:** 1.0  
**Status:** Frozen Requirements  
**Project type:** Personal DIY Robot  
**Primary users:** Chủ sở hữu và người yêu  
**Language:** Tiếng Việt  

---

## 1. Tầm nhìn

ARIA là robot AI đồng hành cá nhân, có khả năng giao tiếp tự nhiên bằng tiếng Việt, tự di chuyển trong nhà, nhận biết người dùng và chủ động tương tác như một người bạn.

ARIA không được thiết kế trước tiên để thương mại hóa. Mục tiêu của V1 là tạo ra một robot thật, ổn định, dễ sử dụng và có thể tiếp tục nâng cấp.

---

## 2. Nguyên tắc thiết kế

1. Ưu tiên khả năng chế tạo thực tế.
2. Ưu tiên trải nghiệm gần gũi hơn thông số phô trương.
3. Dễ sửa chữa và thay thế linh kiện.
4. Không phụ thuộc duy nhất vào một nhà cung cấp AI.
5. Chức năng an toàn phải hoạt động kể cả khi mất Internet.
6. AI không được trực tiếp điều khiển PWM động cơ.
7. Mọi hành động nhạy cảm phải có xác nhận của người dùng.
8. Không tuyên bố ARIA có ý thức thật.

---

## 3. Yêu cầu chức năng đã đóng băng

### 3.1 Giao tiếp AI

ARIA phải:

- trò chuyện bằng tiếng Việt;
- hỗ trợ ChatGPT;
- hỗ trợ Gemini;
- chuyển đổi giữa các AI;
- có trí nhớ riêng;
- có cá tính riêng;
- có khả năng trả lời theo kiểu bạn bè, cà khịa nhẹ;
- không dùng lời lẽ xúc phạm nặng hoặc thao túng cảm xúc.

Ví dụ phong cách:

- “Ơ, gọi gì mày?”
- “Tạm ổn. Phòng 35°C, sắp chín rồi.”
- “Được thôi.”

### 3.2 Giọng nói

ARIA phải:

- có wake word “ARIA”;
- nghe tiếng gọi từ xa trong cùng phòng;
- xác định hướng âm thanh;
- nhận dạng giọng nói tiếng Việt;
- trả lời bằng giọng nói tiếng Việt;
- có phản hồi thị giác ngay khi nghe thấy người dùng;
- xử lý lệnh an toàn và lệnh cơ bản không cần Internet.

### 3.3 Tự tìm người gọi

Khi người dùng gọi “ARIA”, robot phải:

1. xác định hướng âm thanh;
2. quay về hướng đó;
3. dùng camera tìm người;
4. dùng cảm biến hiện diện xác nhận;
5. tránh vật cản;
6. tiến lại gần;
7. dừng cách người dùng khoảng 0,8–1,2 m;
8. không tiếp tục tiến nếu mất dấu người.

### 3.4 Tự hành

ARIA phải:

- di chuyển bằng hai bánh chủ động;
- quay tại chỗ;
- đọc encoder;
- sử dụng IMU;
- tránh vật cản;
- chống rơi cầu thang;
- có bumper vật lý;
- dừng khi cảm biến lỗi;
- dừng khi bộ xử lý chính mất kết nối;
- hoạt động với tốc độ an toàn trong nhà.

### 3.5 Camera và nhận diện

ARIA phải:

- có camera góc rộng;
- phát hiện người;
- theo dõi người trong cùng phòng;
- có thể nhận diện chủ nhân khi người dùng cho phép;
- có LED báo camera hoạt động;
- có công tắc tắt camera phần cứng.

### 3.6 Cảm biến hiện diện

ARIA phải:

- có radar mmWave hoặc cảm biến hiện diện tương đương;
- phát hiện có người trong phòng;
- hoạt động trong điều kiện thiếu sáng;
- hỗ trợ đánh thức robot khi có người xuất hiện.

### 3.7 Màn hình

ARIA phải có màn hình đủ lớn để:

- hiển thị mắt;
- hiển thị biểu cảm;
- hiển thị trạng thái nghe, nghĩ và nói;
- hiển thị nhiệt độ và độ ẩm;
- hiển thị pin;
- hiển thị Wi-Fi và Bluetooth;
- hiển thị YouTube hoặc ứng dụng;
- hiển thị cuộc gọi video khi nền tảng cho phép.

### 3.8 Ứng dụng và giải trí

ARIA phải:

- kết nối Wi-Fi;
- kết nối Bluetooth;
- chạy YouTube;
- phát nhạc;
- hỗ trợ ứng dụng trên hệ điều hành chính;
- có thể mở ứng dụng bằng giọng nói;
- có thể hoạt động như loa Bluetooth hoặc loa mạng.

### 3.9 Cuộc gọi

ARIA phải:

- mở ứng dụng gọi điện hoặc video;
- hiển thị khuôn mặt người gọi trên màn hình;
- thông báo ai đang gọi nếu ứng dụng cung cấp dữ liệu;
- hỗ trợ nhận hoặc từ chối cuộc gọi bằng giọng nói khi hệ điều hành cho phép.

Không cam kết tự động hóa toàn bộ cuộc gọi Messenger nếu nền tảng không cung cấp API phù hợp.

### 3.10 Nhiệt độ và độ ẩm

ARIA phải:

- đo nhiệt độ phòng;
- đo độ ẩm phòng;
- hiển thị số đo;
- trả lời bằng giọng nói;
- đặt cảm biến xa nguồn nhiệt nội bộ;
- cho phép hiệu chỉnh sai số.

### 3.11 Cá tính và tính chủ động

ARIA phải:

- có Persona Engine;
- có Memory Manager;
- có trạng thái nội tại;
- có khả năng chủ động vừa đủ;
- biết khi nào nên nói;
- biết khi nào nên im lặng;
- tự chuyển giọng điệu tùy ngữ cảnh;
- không làm phiền liên tục;
- không giả vờ sợ bị tắt nguồn;
- không tạo cảm giác tội lỗi cho người dùng.

### 3.12 Ứng dụng điện thoại

Ứng dụng phải hỗ trợ:

- xem pin;
- xem nhiệt độ và độ ẩm;
- điều khiển robot;
- chọn ChatGPT hoặc Gemini;
- thay đổi mức độ cà khịa;
- quản lý trí nhớ;
- bật hoặc tắt camera, micro và tính năng chủ động;
- cập nhật phần mềm;
- xem lỗi hệ thống.

### 3.13 Quyền riêng tư

ARIA phải có:

- công tắc tắt micro phần cứng;
- công tắc tắt camera phần cứng;
- LED báo trạng thái camera;
- LED báo trạng thái micro;
- khả năng xóa trí nhớ người dùng;
- khả năng tắt nhận diện khuôn mặt;
- dữ liệu cá nhân lưu cục bộ khi có thể.

---

## 4. Kiến trúc cấp cao

ARIA sử dụng hai tầng xử lý:

### Bộ xử lý chính

Phụ trách:

- hệ điều hành;
- ứng dụng;
- ChatGPT và Gemini;
- camera;
- giao diện;
- nhận dạng tiếng nói;
- tổng hợp giọng nói;
- trí nhớ;
- cá tính;
- lập kế hoạch hành vi.

### Bộ điều khiển thời gian thực (chưa mua; ESP32-S3 chỉ là ứng viên)

Phụ trách:

- động cơ;
- encoder;
- IMU;
- cảm biến vật cản;
- cảm biến chống rơi;
- bumper;
- giám sát pin;
- watchdog;
- dừng khẩn cấp.

---

## 5. Kích thước và ngân sách

- Kích thước 15 × 15 × 15 cm chỉ là mục tiêu ban đầu.
- Kích thước cuối cùng được quyết định sau khi dựng mô hình linh kiện thật.
- Ưu tiên nhỏ gọn nhưng không đánh đổi quá mức về nhiệt, âm thanh và an toàn.
- Ngân sách mục tiêu ban đầu khoảng 6.000.000 đồng.
- Có thể điều chỉnh khi camera, màn hình, micro và nguồn được chốt.

---

## 6. Phạm vi V1

V1 bắt buộc có:

- ChatGPT;
- Gemini;
- hội thoại tiếng Việt;
- màn hình;
- camera;
- cảm biến hiện diện;
- tự hành;
- tìm người gọi trong cùng phòng;
- tránh vật cản;
- chống rơi;
- nhiệt độ và độ ẩm;
- Wi-Fi;
- Bluetooth;
- YouTube;
- cá tính;
- trí nhớ;
- ứng dụng điều khiển cơ bản.

---

## 7. Ngoài phạm vi V1

Các chức năng sau để dành cho V2:

- tự về dock;
- tự tìm người giữa nhiều phòng;
- SLAM chính xác;
- PCB tích hợp hoàn toàn;
- sản xuất hàng loạt;
- tự động hóa toàn bộ Messenger;
- nhận diện cảm xúc nâng cao;
- điều khiển thiết bị nhà thông minh.

---

## 8. Tiêu chí nghiệm thu V1

ARIA V1 được coi là đạt khi:

1. nghe được wake word trong phòng;
2. hội thoại tiếng Việt hoạt động;
3. chuyển được giữa ChatGPT và Gemini;
4. mở được YouTube;
5. hiển thị mắt và trạng thái;
6. tự di chuyển an toàn;
7. tránh được vật cản;
8. không lao xuống cầu thang;
9. tìm và tiến đến người gọi trong cùng phòng;
10. đo được nhiệt độ và độ ẩm;
11. hoạt động được khi mất Internet ở các chức năng an toàn;
12. có thể tắt camera và micro bằng phần cứng.

---

## 9. Quy tắc thay đổi yêu cầu

Tài liệu này là bản yêu cầu đóng băng.

Mọi thay đổi lớn phải:

1. được ghi rõ lý do;
2. đánh giá ảnh hưởng đến chi phí, kích thước và phần mềm;
3. tạo phiên bản mới;
4. không sửa âm thầm vào bản đã đóng băng.

Phiên bản tiếp theo sẽ dùng tên:

- ARIA-PRD-001 Rev B
- ARIA-PRD-001 Rev C

---

## 10. Trạng thái hiện tại

- M0 — Frozen Requirements: hoàn thành
- M1 — Hardware Platform Selection: hoàn thành
- M2 — Danh sách linh kiện đã mua được đồng bộ ngày 2026-08-10; còn bước xác minh hàng thực tế
- M3 — CAD: 1 file đúng tên model chưa kiểm kích thước, 1 file sai một phần, 13 hạng mục chưa có CAD
- M4 — Bench Prototype: chưa bắt đầu
