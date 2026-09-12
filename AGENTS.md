# ARIA working rules

- Cross-task continuity: before working in Codex or ChatGPT Work, fetch/read current GitHub main and docs/ARIA-MASTER-HANDOFF.md. After each completed work block, record decisions, actual evidence, limitations and next action in that same master, then commit/push and verify remote. Do not require the owner to reconstruct prior chat. Unavailable chat/files are not evidence; do not claim account-wide memory sync. Avoid concurrent edits to another active task's files.
- CURRENT HOLD (2026-09-13): pause all motor/encoder/driver development and hardware actions at owner request. Active work is standalone Pi sensor code and audio. Do not start aria-core.service, flash ESP or energize drivers under synchronization authority.

- Read docs/ARIA-MASTER-HANDOFF.md first; preserve its NEXT STEP ORDER and verification boundaries.
- Codex remains primary author and integration reviewer. Use GitHub Copilot for concrete bounded assistance when it saves work; do not duplicate the same full task across assistants.
- Copilot CLI: D:/UserData/ARIA/tools/copilot/bin/copilot.exe. Set COPILOT_HOME=D:/UserData/ARIA/tools/copilot/state and COPILOT_AUTO_UPDATE=false for invocations. Keep work, logs and outputs on D.
- Give Copilot only relevant context and a short output contract. Use an isolated branch/worktree for edits; review its diff and run appropriate checks before integration. Read-only review can use supplied excerpts without tools.
- Never interpret a Copilot answer as hardware evidence. Captures, pinmap, tuning, PRD and last-known-good code remain protected by master rules.
- Check available Codex usage before substantial work blocks. If a reported remaining limit reaches 20% or less, warn the user and checkpoint the current work early. This is an active-session practice, not background monitoring or a guarantee against exhaustion.
- Save completed decisions in the existing master and commit completed changes. Do not repeat whole-file reads or regenerate code unnecessarily; keep user updates concise.
- Copilot and Codex have separate quotas. Do not buy credits, enable overages or use external API billing without the user's instruction.

- User authorizes ongoing GitHub synchronization: after a completed, reviewed work block, commit and push to origin/main, then verify remote HEAD. Fetch before publishing; never force-push or overwrite other work. Report sync failures and retain local changes. This authorization does not permit hardware deployment or paid overages.
