# ARIA Automation — CURRENT/CANONICAL

Status: CURRENT/CANONICAL
Created: 2026-09-19
Scope: ARIA PC automation only.

This is the single source of truth for the ARIA automation system. Do not create a second automation master, handoff, roadmap, or state document. Phase 1 operational state lives under `D:\UserData\ARIA\automation-state`. Phase 2 task packets live under the Git-ignored `automation/runtime/tasks`; runtime data is evidence, not a competing canonical.

## Hard boundaries

- Automation work must not modify PCB, app/UI, firmware, CAD, BOM, wiring, or other project-domain data unless a future user task explicitly targets that domain.
- Existing project holds remain authoritative. Automation cannot release a hold by itself.
- The automation stack is the already selected stack only: ChatGPT/C2C, Codex, repository files, Windows Task Scheduler, and local scripts. Do not add another model, agent framework, tunnel, database, or orchestration service without an explicit decision recorded here.
- One user task enters once and produces one final result. Internal stages may create evidence/checkpoints but do not require repeated user re-entry.
- Codex execution is forbidden before the council emits the exact gate `PASS_TO_EXECUTE` for the same task ID and task digest.
- Every state transition must be resumable from durable checkpoint data.

## Pipeline

| Phase | Component | Required gate |
|---|---|---|
| 0 | Canonical + boundaries | `PHASE_0_PASS` |
| 1 | C2C auto-start + health across Windows logon/reboot | `PHASE_1_PASS` |
| 2 | One-Shot Runner, one input/one output | `PHASE_2_PASS` |
| 3 | Codebase/Project Memory loader by domain | `PHASE_3_PASS` |
| 4 | Engineer Router | `PHASE_4_PASS` |
| 5 | Engineer Council + consensus/pass-fail | `PASS_TO_EXECUTE` or `FAIL_COUNCIL` |
| 6 | Codex executor | `EXECUTION_COMPLETE` or `EXECUTION_FAILED` |
| 7 | Automated verification | `VERIFY_PASS` or `VERIFY_FAIL` |
| 8 | Post-execution review | `POST_REVIEW_PASS` or `POST_REVIEW_FAIL` |
| 9 | Retry/resume/checkpoint | `TASK_PASS` or bounded terminal failure |
| 10 | One-button launcher | launcher acceptance gate |
| 11 | Windows startup integration | startup acceptance gate |

## Domain memory policy

The loader must select canonical material by task domain instead of rereading the whole repository.

- Automation: this file.
- PCB: `docs/ARIA-PCB-PRO-MAX-CANONICAL.md` plus only files named by that canonical/task.
- General project/runtime: `docs/ARIA-MASTER-HANDOFF.md` plus only task-relevant files.
- App/UI: master + task-relevant app files.
- Unknown/mixed: master first, then router-selected domain canonical(s).

Historical conversation exports, old workspaces, build artifacts, and runtime checkpoints are never promoted to canonical merely because they contain matching words.

## Phase 0 evidence — 2026-09-19

- Working repository verified at `D:\UserData\ARIA\repo`.
- Repository was already dirty before automation work, including existing PCB/app/master changes. Automation changes must remain isolated from those pre-existing edits.
- `AGENTS.md` and current `docs/ARIA-MASTER-HANDOFF.md` were read before implementation.
- No prior ARIA automation pipeline matching this architecture was found in the repository.
- C2C runtime was observed under `%USERPROFILE%\.codex-chatgpt-web` with local serve, native MCP, and tunnel-client processes active.

Gate: `PHASE_0_PASS`.

## Phase 1 contract

Phase 1 manages only the existing C2C runtime. It discovers the current runtime command, port, broker socket, tunnel binary and tunnel profile from `%USERPROFILE%\.codex-chatgpt-web\config.json`; it does not pin a release directory.

Health requires all of the following:

1. C2C `serve` process present.
2. Configured local TCP port accepting connections.
3. `tunnel-client` process present for the configured profile.
4. Tunnel health URL file present and HTTP health endpoint returns 200.
5. Native MCP process present.
6. Upstream app name matches `Codex Native2`.

Windows integration uses two idempotent user-level scheduled tasks: one at logon and one watchdog every five minutes. Both call the same `Ensure` action. The manager only starts missing components; it does not kill a live C2C process during normal watchdog operation.

Reboot acceptance is self-recording: after a later reboot/logon, a successful scheduled `Ensure` refreshes `D:\UserData\ARIA\automation-state\c2c-health.json`. The implementation gate can pass in the current session when live health, idempotence and task definitions pass; the first post-reboot record is additional runtime evidence.

## Phase 1 evidence — 2026-09-19

Windows Task Scheduler contains exactly the two canonical ARIA C2C tasks; no additional task matching `ARIA-C2C-*` was present.

| Task | State | Enabled | Trigger | Action | Working directory |
|---|---|---:|---|---|---|
| `ARIA-C2C-Startup` | Ready | Yes | User logon | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\UserData\ARIA\repo\automation\windows\aria-c2c.ps1" Ensure` | `D:\UserData\ARIA\repo` |
| `ARIA-C2C-Watchdog` | Ready | Yes | Time trigger repeated every 5 minutes | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\UserData\ARIA\repo\automation\windows\aria-c2c.ps1" Ensure` | `D:\UserData\ARIA\repo` |

Both tasks use `StartWhenAvailable=true`, `MultipleInstances=IgnoreNew`, `RestartCount=3`, and `RestartInterval=PT1M`. The watchdog's recovery run completed with Task Scheduler result `0`.

Controlled recovery evidence:

- Baseline watchdog run: `2026-09-19T20:52:10+09:00`; next scheduled run: `2026-09-19T20:57:09+09:00`.
- At `2026-09-19T20:57:08.5229192+09:00`, only the matched C2C `serve` PID 21148 and `tunnel-client` PID 23420 for profile `codex-chatgpt-web` were stopped. Native MCP PID 6992 was explicitly preserved; unrelated Codex/ChatGPT processes were not targeted.
- The watchdog ran at `2026-09-19T20:57:10+09:00` and restored full health by `2026-09-19T20:57:16.2403920+09:00`, 7.717 seconds after the controlled stop.
- Recovery result: serve present, tunnel present, native MCP present, `127.0.0.1:17841` listening, tunnel health HTTP 200, watchdog result `0`.
- A later independent health read at `2026-09-19T21:01:51.8455265+09:00` returned `ready=true`, serve count 1, tunnel count 2, native MCP count 2, local port healthy, and tunnel HTTP 200. The two tunnel/MCP pairs used the same canonical C2C profile; Phase 1 health requires at least one healthy instance. Scheduled-task duplication remained absent.
- The required post-recovery test `automation\tests\test-phase1.ps1` completed successfully at `2026-09-19T21:01:53.7265515+09:00` with gate `PHASE_1_PASS`, C2C ready, local port 17841, tunnel HTTP 200, and both canonical task names.
- First reboot/logon evidence remains self-recording as specified by the Phase 1 contract and is not required for this current-session implementation gate.

Gate: `PHASE_1_PASS`.

## Phase 2 contract

`automation/runner/aria-runner.ps1` is the only Phase 2 intake entrypoint. It accepts either one text request or one JSON task file, normalizes the input into a machine-readable packet, determines the ARIA Git workspace, reads and hashes this canonical plus `AGENTS.md`, checks the Phase 0 and Phase 1 gates and live C2C health, then stops at the routing boundary.

The fixed Phase 2 state machine is:

`RECEIVED -> CONTEXT_LOAD -> PRECHECK -> READY_FOR_ROUTING -> STOP`

Phase 2 does not start the memory loader, Engineer Router, Engineer Council, Codex execution, repository execution, automated verification, or post-execution review. `READY_FOR_ROUTING` records readiness for a future phase; it is not `PASS_TO_EXECUTE`.

Each task uses `automation/runtime/tasks/<task_id>/` and contains `task.json`, `checkpoint.json`, `events.jsonl`, and `final-report.json`. The raw user request is stored only in `task.json`; checkpoints and events retain hashes, stage state, and bounded evidence. Task text, task-file size, and event count have configured limits. Mutable JSON files use same-directory temporary writes followed by replacement, and a per-task file lock prevents concurrent attempts.

`checkpoint.json` is the durable resume authority. A controlled interruption leaves the next stage and status `INTERRUPTED`; a failure records the failed stage as `resume_stage`, enters `STOP`, emits one aggregate failure report, and exits nonzero. Resume verifies the immutable task digest, increments `attempt_count`, and continues from the saved stage. A completed task is idempotent: resume returns the existing final report without rerunning stages.

## Phase 2 evidence — 2026-09-19

- Added the single runner plus machine-readable task/checkpoint schemas and fixed stage definition under `automation/runner/`.
- Added a Git-ignored runtime packet root at `automation/runtime/tasks` and configured bounded input/event limits in `automation/config.json`.
- `automation/tests/test-phase2.ps1` passed at `2026-09-19T21:12:41.1543280+09:00`: text input, JSON input, controlled interruption, durable resume, safe failure stop, packet files, no raw-context duplication, and live C2C precheck all passed. The final stage was `STOP`; routing and Codex execution remained false.
- Acceptance task `aria-20260919T211253-3323fe10` ran through Windows `powershell.exe` with exit code 0 and one aggregate output. It completed `RECEIVED`, `CONTEXT_LOAD`, `PRECHECK`, and `READY_FOR_ROUTING`, then stopped with result `READY_FOR_ROUTING`.
- The acceptance packet contains all four required files. `task.json` and `checkpoint.json` passed their JSON Schemas; all 10 event lines parsed; checkpoint status is `COMPLETED`, current stage is `STOP`, allowed write scope contains only that task packet directory, and the raw request occurs zero times outside `task.json`.
- Acceptance precheck verified repository `D:\UserData\ARIA\repo`, Phase 0 PASS, Phase 1 PASS, C2C ready on port 17841, and tunnel health HTTP 200.
- No PCB, app/UI, firmware, CAD, BOM, wiring, router, council, or executor work was performed by the runner or its tests.

Gate: `PHASE_2_PASS`.

## Current phase state

- Phase 0: PASS.
- Phase 1: PASS.
- Phase 2: PASS.
- Phase 3+: NOT STARTED; blocked until separately implemented and accepted.
