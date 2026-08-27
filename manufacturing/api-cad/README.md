# ARIA final CAD/API workspace

Đây là **điểm vào bắt buộc** cho mọi người, API, agent hoặc script làm CAD cơ khí final của ARIA.

## Quy tắc authority

1. Branch `main` của `bapngo002/ARIA` là Single Source of Truth của dự án. Bộ workspace này được tạo từ snapshot `main@e3a6a83f4384d188aee4c76c771f4b8fce5c523e` ngày 2026-08-27.
2. Danh tính, số lượng và trạng thái mua linh kiện vẫn chỉ lấy từ [`purchased-hardware/README.md`](../../purchased-hardware/README.md). `ARIA-COMPONENT-INVENTORY.md` ở đây là **bảng readiness/instance cho CAD**, không phải BOM hoặc purchase register thứ hai.
3. Khi làm CAD, đọc theo thứ tự:
   1. file này;
   2. `ARIA-CAD-MASTER-SPEC.md`;
   3. `ARIA-CONSTRAINTS.json`;
   4. `ARIA-OBJECT-MAP.json`;
   5. `ARIA-WORKFLOW.md`;
   6. `ARIA-VALIDATION-CHECKLIST.md`.
4. Không đọc lịch sử chat để bổ sung kích thước, orientation hoặc constraint. Các quyết định đã duyệt từ giai đoạn trao đổi được đóng băng lại trong workspace này; chat không còn là đầu vào runtime.
5. Không dùng file CAD cũ, file trong `cad-review/`, file ngoài repo hoặc object có `Label` gần giống nếu file/object đó chưa được duyệt và map rõ trong `ARIA-OBJECT-MAP.json`.
6. Không suy kích thước từ ảnh, listing, tên chuẩn chung như “3010”, hoặc bounding box của model sai. Không scale toàn bộ model để sửa một feature sai.
7. `UNKNOWN`, `PENDING`, `NOT_MAPPED` hoặc `NOT_VERIFIED` **không tự động là blocker**. Nếu item đã có assembly thực, envelope hoặc constraint đủ để bố trí, tiếp tục bằng placeholder được duyệt và ghi rõ phạm vi không được dùng để chế tạo.
8. Chỉ `TRUE_BLOCKER` mới chặn `FINAL_RELEASE`: dữ liệu bắt buộc để khóa hình học chế tạo mà không thể tính từ assembly/layout, không thể dùng envelope bảo thủ và không thể thay bằng giao diện điều chỉnh được.
9. Không yêu cầu người dùng nhập lại quyết định đã có trong master spec/constraints/inventory. Chỉ hỏi dữ liệu đo hoặc lựa chọn thực sự còn là `TRUE_BLOCKER` khi sắp khóa đúng interface chế tạo phụ thuộc vào nó.
10. Mọi output phải ghi source commit, input SHA-256, phiên bản constraint, kết quả validation và các deviation đã được người dùng duyệt.

## Ý nghĩa trạng thái

- `CAD_EXACT`: đúng model và các kích thước critical đã được kiểm tra; có thể dùng làm authority hình học. Hiện snapshot repo chưa có model nào đạt release gate này.
- `ASSEMBLY_LOCKED`: cụm tích hợp; chỉ được transform cả cụm như rigid body, không đổi hình học/vị trí tương đối bên trong.
- `ENVELOPE_ONLY`: chỉ dựng khối bao/datum đã khóa; không thiết kế cấu tạo bên trong.
- `PENDING`: còn dữ liệu cần hoàn thiện. Trạng thái này được phân loại tiếp thành `NON_BLOCKING` hoặc `TRUE_BLOCKER`; bản thân từ `PENDING` không buộc dừng layout.
- `DESIGN_NEW`: chi tiết phải tạo mới theo constraint đã khóa và kiểm tra bằng checklist.

## Hai gate độc lập

- `LAYOUT`: được tiếp tục khi mỗi item có ít nhất một trong ba authority: assembly thực, envelope hoặc constraint cơ khí đủ dùng. Placeholder phải có tên rõ, màu/metadata `PLACEHOLDER`, và không được dùng để khoan lỗ hoặc tạo interface chế tạo chưa biết.
- `FINAL_RELEASE`: chỉ PASS khi mọi `true_blockers_final` đã được giải quyết và checklist chế tạo có evidence.

Thiếu exact CAD nhưng có envelope không phải blocker. Thiếu mapping object trong repo nhưng có assembly thực trong file làm việc cũng không phải blocker. Các mount chưa biết có thể dùng slot, clamp, cradle, carrier thay được hoặc chừa vùng service bảo thủ trong giai đoạn layout.

## Phạm vi và cấu trúc

```text
manufacturing/api-cad/
├── README.md
├── ARIA-CAD-MASTER-SPEC.md
├── ARIA-COMPONENT-INVENTORY.md
├── ARIA-CONSTRAINTS.json
├── ARIA-OBJECT-MAP.json
├── ARIA-WORKFLOW.md
├── ARIA-VALIDATION-CHECKLIST.md
├── input/
│   ├── cad/
│   ├── measurements/
│   └── reference-images/
├── scripts/
└── output/
    ├── reports/
    └── export/
```

- `input/cad/`: bản sao làm việc của FCStd/STEP/DWG đã được duyệt hoặc file assembly cần scan; không tự động hợp thức hóa file chỉ vì nó nằm trong thư mục.
- `input/measurements/`: phép đo phần cứng thật, có đơn vị, dụng cụ, ngày đo và người xác nhận.
- `input/reference-images/`: chỉ tham chiếu ngoại hình/kiểm chứng; không được đo kích thước từ pixel.
- `output/reports/`: object scan, preflight, collision/clearance/optical/acoustic/airflow/assembly reports.
- `output/export/`: chỉ chứa export sau khi toàn bộ critical checks PASS và được duyệt release.

## Gate hiện tại

Workspace đã đủ điều kiện **tiếp tục layout bằng assembly/envelope/placeholder**. Chưa được gắn nhãn `RELEASED FOR MANUFACTURE` cho tới khi giải quyết các `TRUE_BLOCKER` final. Chạy:

```text
python scripts/01_validate_workspace.py --stage layout
```

để xác nhận layout có thể tiếp tục. Trước khi export chế tạo, chạy:

```text
python scripts/01_validate_workspace.py --stage final-release
```

Final-release preflight phải thất bại cho tới khi mọi `TRUE_BLOCKER` bắt buộc thực sự được giải quyết.
