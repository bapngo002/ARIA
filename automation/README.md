# ARIA Automation

Canonical state and architecture: `docs/ARIA-AUTOMATION-CANONICAL.md`.

Runtime state is kept outside Git at `D:\UserData\ARIA\automation-state`.

Phase 1 commands:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\windows\aria-c2c.ps1 Status
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\windows\aria-c2c.ps1 Ensure
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\windows\install-c2c-startup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\tests\test-phase1.ps1
```

Phase 2 one-shot runner:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\runner\aria-runner.ps1 -TaskText "Review current PRO MAX power state"
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\runner\aria-runner.ps1 -TaskFile .\task.json
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\runner\aria-runner.ps1 -ResumeTaskId aria-YYYYMMDDTHHMMSS-xxxxxxxx
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\tests\test-phase2.ps1
```

Phase 2 task packets are untracked runtime data under `automation/runtime/tasks/<task_id>`. See `automation/runner/README.md` for the state machine and packet contract.
