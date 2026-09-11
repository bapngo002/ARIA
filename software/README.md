# ARIA software

Source capture Pi nằm trong [pi/](pi/); unit được bảo tồn tại pi/aria-core.service. [capture-manifest.json](capture-manifest.json) lưu SHA-256 và nguồn. Không dùng pip-freeze.txt như môi trường tái dựng đã verified. Model/Whisper mới có danh sách đường dẫn.

Trạng thái, giới hạn runtime, IPC và checklist duy nhất nằm trong [MASTER HANDOFF](../docs/ARIA-MASTER-HANDOFF.md). Không tự deploy snapshot trước khi đối chiếu thiết bị.
