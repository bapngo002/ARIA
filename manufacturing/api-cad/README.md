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
7. Giá trị `UNKNOWN`, `PENDING`, `NOT_MAPPED` hoặc `NOT_VERIFIED` ở trường critical là **điều kiện dừng**. Báo đúng object/trường thiếu; không tự điền giá trị giả để chạy tiếp.
8. Mọi output phải ghi source commit, input SHA-256, phiên bản constraint, kết quả validation và các deviation đã được người dùng duyệt.

## Ý nghĩa trạng thái

- `CAD_EXACT`: đúng model và các kích thước critical đã được kiểm tra; có thể dùng làm authority hình học. Hiện snapshot repo chưa có model nào đạt release gate này.
- `ASSEMBLY_LOCKED`: cụm tích hợp; chỉ được transform cả cụm như rigid body, không đổi hình học/vị trí tương đối bên trong.
- `ENVELOPE_ONLY`: chỉ dựng khối bao/datum đã khóa; không thiết kế cấu tạo bên trong.
- `PENDING`: thiếu file, mapping, đo đạc hoặc xác minh critical; không được release geometry phụ thuộc vào dữ liệu đó.
- `DESIGN_NEW`: chi tiết phải tạo mới theo constraint đã khóa và kiểm tra bằng checklist.

Một item có thể mang `ASSEMBLY_LOCKED` hoặc `DESIGN_NEW` về vai trò thiết kế nhưng vẫn có gate `PENDING` ở input. Trường `release_blockers` trong object map quyết định có được đi tiếp hay không.

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

Workspace này đã khóa phương án và chuẩn bị quy trình, nhưng **chưa được phép tạo bản CAD chế tạo** vì chưa có/mapping được FreeCAD assembly tích hợp cùng nhiều model critical. Chạy:

```text
python scripts/01_validate_workspace.py --allow-pending
```

để kiểm cấu trúc/JSON. Bỏ `--allow-pending` để chạy release preflight nghiêm ngặt; preflight phải thất bại cho tới khi mọi blocker critical được giải quyết.
