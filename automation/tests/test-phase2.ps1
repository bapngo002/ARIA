[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$AutomationRoot = Join-Path $RepoRoot 'automation'
$Runner = Join-Path $AutomationRoot 'runner\aria-runner.ps1'
$SandboxRoot = Join-Path $AutomationRoot ('runtime\test-sandbox\phase2-' + [guid]::NewGuid().ToString('N'))
$RuntimeRoot = Join-Path $SandboxRoot 'runtime'
$PowerShellExe = (Get-Process -Id $PID).Path

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
}

function Read-JsonFile {
    param([string]$Path)
    Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}

$sandboxFull = [System.IO.Path]::GetFullPath($SandboxRoot)
$automationFull = [System.IO.Path]::GetFullPath($AutomationRoot).TrimEnd('\')
if (-not $sandboxFull.StartsWith($automationFull + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Refusing to use a test sandbox outside automation.'
}

New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null

try {
    foreach ($schema in @('task-schema.json', 'checkpoint-schema.json', 'stage-schema.json')) {
        $null = Read-JsonFile (Join-Path $AutomationRoot "runner\$schema")
    }

    $request = 'Phase 2 sandbox resume acceptance task'
    $firstRaw = & $Runner -TaskText $request -RuntimeRoot $RuntimeRoot -StopAfterStage PRECHECK
    $first = $firstRaw | ConvertFrom-Json
    Assert-True ($first.status -eq 'INTERRUPTED') 'Runner did not record INTERRUPTED.'
    Assert-True ($first.result -eq 'INTERRUPTED_RESUMABLE') 'Interrupted result is incorrect.'
    Assert-True ($first.current_stage -eq 'READY_FOR_ROUTING') 'Checkpoint did not advance to the resumable stage.'

    $taskId = [string]$first.task_id
    $taskDirectory = Join-Path $RuntimeRoot "tasks\$taskId"
    foreach ($name in @('task.json', 'checkpoint.json', 'events.jsonl', 'final-report.json')) {
        Assert-True (Test-Path -LiteralPath (Join-Path $taskDirectory $name) -PathType Leaf) "Missing task artifact: $name"
    }

    $resumeRaw = & $Runner -ResumeTaskId $taskId -RuntimeRoot $RuntimeRoot
    $resumed = $resumeRaw | ConvertFrom-Json
    Assert-True ($resumed.status -eq 'COMPLETED') 'Resumed task did not complete.'
    Assert-True ($resumed.result -eq 'READY_FOR_ROUTING') 'Resumed task did not reach routing readiness.'
    Assert-True ($resumed.current_stage -eq 'STOP') 'Resumed task did not stop at Phase 2 boundary.'
    Assert-True ($resumed.attempt_count -eq 2) 'Resume did not increment attempt_count.'
    Assert-True (-not $resumed.phase_boundaries.routing_started) 'Router started during Phase 2.'
    Assert-True (-not $resumed.phase_boundaries.codex_execution_started) 'Codex execution started during Phase 2.'

    $task = Read-JsonFile (Join-Path $taskDirectory 'task.json')
    $checkpoint = Read-JsonFile (Join-Path $taskDirectory 'checkpoint.json')
    Assert-True ($task.user_request -eq $request) 'Normalized task request changed.'
    Assert-True ($task.allowed_paths.Count -eq 1) 'Phase 2 allowed_paths must contain only the packet directory.'
    Assert-True ($task.allowed_paths[0] -eq $taskDirectory) 'allowed_paths does not target the packet directory.'
    Assert-True ($checkpoint.completed_stages.Count -eq 4) 'Not all Phase 2 stages were completed exactly once.'
    Assert-True ($checkpoint.stage_evidence.CONTEXT_LOAD.raw_context_copied -eq $false) 'Raw canonical context was copied.'
    Assert-True ($checkpoint.stage_evidence.PRECHECK.c2c_ready -eq $true) 'C2C precheck is not healthy.'

    foreach ($name in @('checkpoint.json', 'events.jsonl', 'final-report.json')) {
        $contents = Get-Content -LiteralPath (Join-Path $taskDirectory $name) -Raw
        Assert-True (-not $contents.Contains($request)) "Raw request was duplicated into $name."
    }

    $jsonInputPath = Join-Path $SandboxRoot 'task-input.json'
    $jsonInput = [ordered]@{ user_request = 'Phase 2 JSON intake acceptance task'; workspace = $RepoRoot; scope = 'automation_test' } | ConvertTo-Json
    [System.IO.File]::WriteAllText($jsonInputPath, $jsonInput, [System.Text.UTF8Encoding]::new($false))
    $jsonRaw = & $Runner -TaskFile $jsonInputPath -RuntimeRoot $RuntimeRoot
    $jsonResult = $jsonRaw | ConvertFrom-Json
    Assert-True ($jsonResult.result -eq 'READY_FOR_ROUTING') 'JSON input did not complete.'
    $jsonTask = Read-JsonFile (Join-Path $RuntimeRoot "tasks\$($jsonResult.task_id)\task.json")
    Assert-True ($jsonTask.input_source.kind -eq 'json_file') 'JSON input source was not recorded.'
    Assert-True ($jsonTask.scope.requested -eq 'automation_test') 'Requested scope was not preserved.'

    $missingWorkspace = Join-Path $SandboxRoot 'missing-workspace'
    $failureInputPath = Join-Path $SandboxRoot 'failure-input.json'
    $failureInput = [ordered]@{ user_request = 'Phase 2 controlled failure acceptance task'; workspace = $missingWorkspace } | ConvertTo-Json
    [System.IO.File]::WriteAllText($failureInputPath, $failureInput, [System.Text.UTF8Encoding]::new($false))
    $failureRaw = & $PowerShellExe -NoProfile -File $Runner -TaskFile $failureInputPath -RuntimeRoot $RuntimeRoot
    $failureExit = $LASTEXITCODE
    $failure = $failureRaw | ConvertFrom-Json
    Assert-True ($failureExit -eq 2) 'Controlled failure did not return exit code 2.'
    Assert-True ($failure.status -eq 'FAILED') 'Controlled failure status is not FAILED.'
    Assert-True ($failure.result -eq 'FAILED_SAFE_STOP') 'Controlled failure did not safe-stop.'
    Assert-True ($failure.current_stage -eq 'STOP') 'Controlled failure did not enter STOP.'
    Assert-True ($failure.resume_stage -eq 'PRECHECK') 'Controlled failure did not preserve resume_stage.'

    [pscustomobject]@{
        gate = 'PHASE_2_PASS'
        timestamp = (Get-Date).ToString('o')
        text_input = 'PASS'
        json_input = 'PASS'
        controlled_interruption = 'PASS'
        resume = 'PASS'
        safe_failure_stop = 'PASS'
        packet_files = 'PASS'
        raw_context_duplication = 'PASS'
        c2c_precheck = 'PASS'
        final_stage = 'STOP'
        routing_started = $false
        codex_execution_started = $false
    } | ConvertTo-Json -Depth 6
}
finally {
    if (Test-Path -LiteralPath $SandboxRoot) {
        $resolved = [System.IO.Path]::GetFullPath($SandboxRoot)
        if ($resolved.StartsWith($automationFull + '\runtime\test-sandbox\', [StringComparison]::OrdinalIgnoreCase)) {
            Remove-Item -LiteralPath $resolved -Recurse -Force
        }
    }
}
