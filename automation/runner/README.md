# ARIA One-Shot Runner — Phase 2

`aria-runner.ps1` is the single Phase 2 intake entrypoint. It accepts one task, creates one durable packet, advances the fixed state machine, and prints one aggregate JSON report. Phase 2 always stops before routing, council, Codex execution, or repository execution.

## Commands

Task text:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\runner\aria-runner.ps1 -TaskText "Review current PRO MAX power state"
```

The task text can also be positional:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\runner\aria-runner.ps1 "Review current PRO MAX power state"
```

JSON input:

```json
{
  "user_request": "Review current PRO MAX power state",
  "workspace": "D:\\UserData\\ARIA\\repo",
  "scope": "review"
}
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\runner\aria-runner.ps1 -TaskFile .\task.json
```

Resume after interruption or a corrected transient failure:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\automation\runner\aria-runner.ps1 -ResumeTaskId aria-YYYYMMDDTHHMMSS-xxxxxxxx
```

## Durable packet

Each task is stored under `automation/runtime/tasks/<task_id>/`:

- `task.json`: the normalized request and immutable task digest.
- `checkpoint.json`: authoritative resumable stage state.
- `events.jsonl`: bounded append-only transition evidence; raw task text is not copied here.
- `final-report.json`: the single aggregate output for the latest attempt.

Writes to `task.json`, `checkpoint.json`, and `final-report.json` use same-directory temporary files and atomic replacement. A per-task lock prevents concurrent attempts. The checkpoint is authoritative if power loss occurs between file writes. A resumed invocation verifies the immutable task digest before continuing.

The Phase 2 state machine is fixed in `stage-schema.json`:

```text
RECEIVED -> CONTEXT_LOAD -> PRECHECK -> READY_FOR_ROUTING -> STOP
```

Any failure records `FAILED`, enters `STOP`, preserves the failed stage in `resume_stage`, writes a final report, and exits with code 2. A successful run exits with code 0 and result `READY_FOR_ROUTING`. `STOP` is a boundary in this phase, not permission to route or execute.
