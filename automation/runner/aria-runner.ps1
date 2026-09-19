[CmdletBinding(DefaultParameterSetName = 'Text')]
param(
    [Parameter(Mandatory, Position = 0, ParameterSetName = 'Text')]
    [Alias('Task')]
    [string]$TaskText,

    [Parameter(Mandatory, ParameterSetName = 'File')]
    [string]$TaskFile,

    [Parameter(Mandatory, ParameterSetName = 'Resume')]
    [string]$ResumeTaskId,

    [string]$Workspace,
    [string]$RuntimeRoot,

    [ValidateSet('RECEIVED', 'CONTEXT_LOAD', 'PRECHECK')]
    [string]$StopAfterStage
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$AutomationRoot = Join-Path $RepoRoot 'automation'
$ConfigPath = Join-Path $AutomationRoot 'config.json'
$Config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$CanonicalRelative = [string]$Config.canonical
$CanonicalPath = Join-Path $RepoRoot $CanonicalRelative
$PolicyPath = Join-Path $RepoRoot 'AGENTS.md'
$StageDefinitionPath = Join-Path $PSScriptRoot 'stage-schema.json'
$TaskIdPattern = '^aria-[0-9]{8}T[0-9]{6}-[a-f0-9]{8}$'
$StageNames = @('RECEIVED', 'CONTEXT_LOAD', 'PRECHECK', 'READY_FOR_ROUTING', 'STOP')
$MaxEvents = [int]$Config.runner.max_events_per_task
$script:EventCount = 0

function Get-IsoTimestamp {
    (Get-Date).ToString('o')
}

function Get-NormalizedPath {
    param([Parameter(Mandatory)][string]$Path)
    [System.IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($Path)).TrimEnd('\', '/')
}

function Test-PathWithin {
    param(
        [Parameter(Mandatory)][string]$Candidate,
        [Parameter(Mandatory)][string]$Parent
    )
    $candidateFull = Get-NormalizedPath $Candidate
    $parentFull = Get-NormalizedPath $Parent
    $candidateFull.Equals($parentFull, [StringComparison]::OrdinalIgnoreCase) -or
        $candidateFull.StartsWith($parentFull + [System.IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
}

function Write-JsonAtomic {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)]$Value
    )
    $directory = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
    $temporary = Join-Path $directory ((Split-Path -Leaf $Path) + '.' + [guid]::NewGuid().ToString('N') + '.tmp')
    $json = $Value | ConvertTo-Json -Depth 20
    [System.IO.File]::WriteAllText($temporary, $json + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $temporary -Destination $Path -Force
}

function Read-Json {
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Required JSON file not found: $Path" }
    Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
}

function Get-Sha256Text {
    param([Parameter(Mandatory)][string]$Text)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
        ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally { $sha.Dispose() }
}

function Get-TaskDigest {
    param($Task)
    $immutable = [ordered]@{
        schema_version = $Task.schema_version
        task_id = $Task.task_id
        created_at = $Task.created_at
        workspace = $Task.workspace
        user_request = $Task.user_request
        input_source = $Task.input_source
        scope = $Task.scope
        canonical_files = @($Task.canonical_files)
        allowed_paths = @($Task.allowed_paths)
        forbidden_paths = @($Task.forbidden_paths)
        required_evidence = @($Task.required_evidence)
    }
    Get-Sha256Text (($immutable | ConvertTo-Json -Depth 12 -Compress))
}

function Add-Event {
    param(
        [Parameter(Mandatory)][string]$EventsPath,
        [Parameter(Mandatory)][string]$TaskId,
        [Parameter(Mandatory)][int]$Attempt,
        [Parameter(Mandatory)][string]$Stage,
        [Parameter(Mandatory)][string]$Event,
        [Parameter(Mandatory)][string]$Message,
        $Evidence = $null
    )
    if ($script:EventCount -ge $MaxEvents) { throw "Event limit reached for task $TaskId ($MaxEvents)." }
    $entry = [ordered]@{
        schema_version = 1
        timestamp = Get-IsoTimestamp
        task_id = $TaskId
        attempt = $Attempt
        stage = $Stage
        event = $Event
        message = $Message
    }
    if ($null -ne $Evidence) { $entry.evidence = $Evidence }
    $line = ($entry | ConvertTo-Json -Depth 12 -Compress) + [Environment]::NewLine
    $encoding = [System.Text.UTF8Encoding]::new($false)
    $stream = [System.IO.FileStream]::new($EventsPath, [System.IO.FileMode]::Append, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
    try {
        $bytes = $encoding.GetBytes($line)
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush($true)
    }
    finally { $stream.Dispose() }
    $script:EventCount++
}

function Set-StageEvidence {
    param($Checkpoint, [string]$Stage, $Evidence)
    if ($Checkpoint.stage_evidence.PSObject.Properties.Name -contains $Stage) {
        $Checkpoint.stage_evidence.$Stage = $Evidence
    }
    else {
        $Checkpoint.stage_evidence | Add-Member -NotePropertyName $Stage -NotePropertyValue $Evidence
    }
}

function Add-CompletedStage {
    param($Checkpoint, [string]$Stage)
    $result = [System.Collections.Generic.List[string]]::new()
    foreach ($item in @($Checkpoint.completed_stages)) {
        if (-not $result.Contains([string]$item)) { $result.Add([string]$item) }
    }
    if (-not $result.Contains($Stage)) { $result.Add($Stage) }
    $Checkpoint.completed_stages = @($result)
}

function Save-State {
    param($Task, $Checkpoint, [string]$TaskPath, [string]$CheckpointPath)
    $Task.current_stage = $Checkpoint.current_stage
    $Task.status = $Checkpoint.status
    $Task.attempt_count = $Checkpoint.attempt_count
    $Checkpoint.updated_at = Get-IsoTimestamp
    Write-JsonAtomic -Path $TaskPath -Value $Task
    Write-JsonAtomic -Path $CheckpointPath -Value $Checkpoint
}

function Assert-TaskPacket {
    param($Task)
    if ([int]$Task.schema_version -ne 1) { throw 'Unsupported task schema version.' }
    if ([string]$Task.task_id -notmatch $TaskIdPattern) { throw 'Invalid task_id.' }
    if ([string]::IsNullOrWhiteSpace([string]$Task.user_request)) { throw 'user_request is empty.' }
    if (([string]$Task.user_request).Length -gt [int]$Config.runner.max_task_text_chars) { throw 'user_request exceeds configured limit.' }
    if ([string]$Task.scope.enforced -ne 'PHASE_2_INTAKE_ONLY') { throw 'Phase 2 scope boundary is missing.' }
    if ($StageNames -notcontains [string]$Task.current_stage) { throw 'Task contains an unknown stage.' }
    if ((Get-TaskDigest $Task) -ne [string]$Task.task_digest) { throw 'Task digest mismatch.' }
}

function Assert-Checkpoint {
    param($Task, $Checkpoint)
    if ([int]$Checkpoint.schema_version -ne 1) { throw 'Unsupported checkpoint schema version.' }
    if ([string]$Checkpoint.task_id -ne [string]$Task.task_id) { throw 'Checkpoint task_id mismatch.' }
    if ([string]$Checkpoint.task_digest -ne [string]$Task.task_digest) { throw 'Checkpoint task digest mismatch.' }
    if ($StageNames -notcontains [string]$Checkpoint.current_stage) { throw 'Checkpoint contains an unknown stage.' }
    if ([int]$Checkpoint.attempt_count -lt 1) { throw 'Invalid checkpoint attempt count.' }
}

function Get-InputValue {
    param($InputObject, [string]$Name)
    if ($null -ne $InputObject -and $InputObject.PSObject.Properties.Name -contains $Name) {
        return $InputObject.$Name
    }
    $null
}

function Resolve-WorkspaceValue {
    param([string]$RequestedPath)
    $candidate = Get-NormalizedPath $RequestedPath
    if (Test-Path -LiteralPath $candidate -PathType Container) {
        $gitRoot = (& git -C $candidate rev-parse --show-toplevel 2>$null | Out-String).Trim()
        if ($LASTEXITCODE -eq 0 -and $gitRoot) { return Get-NormalizedPath $gitRoot }
    }
    $candidate
}

function New-FinalReport {
    param($Task, $Checkpoint, [int]$EventsCount)
    $result = switch ([string]$Checkpoint.status) {
        'COMPLETED' { 'READY_FOR_ROUTING' }
        'INTERRUPTED' { 'INTERRUPTED_RESUMABLE' }
        'FAILED' { 'FAILED_SAFE_STOP' }
        default { 'INCOMPLETE' }
    }
    [ordered]@{
        schema_version = 1
        task_id = [string]$Task.task_id
        task_digest = [string]$Task.task_digest
        generated_at = Get-IsoTimestamp
        status = [string]$Checkpoint.status
        result = $result
        current_stage = [string]$Checkpoint.current_stage
        resume_stage = $Checkpoint.resume_stage
        attempt_count = [int]$Checkpoint.attempt_count
        workspace = [string]$Task.workspace
        completed_stages = @($Checkpoint.completed_stages)
        evidence = $Checkpoint.stage_evidence
        events_count = $EventsCount
        last_error = $Checkpoint.last_error
        phase_boundaries = [ordered]@{
            routing_started = $false
            council_started = $false
            codex_execution_started = $false
            repository_execution_started = $false
        }
    }
}

$configuredRuntime = if ($RuntimeRoot) { $RuntimeRoot } else { [string]$Config.runner.runtime_root }
$RuntimeRootPath = Get-NormalizedPath $configuredRuntime
if (-not (Test-PathWithin -Candidate $RuntimeRootPath -Parent $AutomationRoot)) {
    throw "Runner runtime root must stay inside the automation namespace: $RuntimeRootPath"
}
$TasksRoot = Join-Path $RuntimeRootPath ([string]$Config.runner.tasks_subdir)
New-Item -ItemType Directory -Force -Path $TasksRoot | Out-Null

$TaskDirectory = $null
$TaskPath = $null
$CheckpointPath = $null
$EventsPath = $null
$FinalReportPath = $null
$LockStream = $null
$TaskObject = $null
$CheckpointObject = $null
$CurrentStage = 'RECEIVED'

try {
    if ($PSCmdlet.ParameterSetName -eq 'Resume') {
        if ($ResumeTaskId -notmatch $TaskIdPattern) { throw 'Invalid resume task_id.' }
        $TaskDirectory = Join-Path $TasksRoot $ResumeTaskId
        if (-not (Test-PathWithin -Candidate $TaskDirectory -Parent $TasksRoot)) { throw 'Resume path escaped the tasks root.' }
        $TaskPath = Join-Path $TaskDirectory 'task.json'
        $CheckpointPath = Join-Path $TaskDirectory 'checkpoint.json'
        $EventsPath = Join-Path $TaskDirectory 'events.jsonl'
        $FinalReportPath = Join-Path $TaskDirectory 'final-report.json'
        if (-not (Test-Path -LiteralPath $TaskDirectory -PathType Container)) { throw "Task not found: $ResumeTaskId" }
    }
    else {
        $inputObject = $null
        $inputKind = 'text'
        $inputFileName = $null
        $request = $TaskText
        $requestedScope = $null
        $requestedWorkspace = $Workspace

        if ($PSCmdlet.ParameterSetName -eq 'File') {
            $inputPath = Get-NormalizedPath $TaskFile
            if (-not (Test-Path -LiteralPath $inputPath -PathType Leaf)) { throw "Task file not found: $inputPath" }
            if ((Get-Item -LiteralPath $inputPath).Length -gt [int]$Config.runner.max_task_file_bytes) { throw 'Task file exceeds configured size limit.' }
            $inputObject = Read-Json $inputPath
            $request = [string](Get-InputValue -InputObject $inputObject -Name 'user_request')
            if (-not $requestedWorkspace) { $requestedWorkspace = [string](Get-InputValue -InputObject $inputObject -Name 'workspace') }
            $requestedScope = Get-InputValue -InputObject $inputObject -Name 'scope'
            $inputKind = 'json_file'
            $inputFileName = Split-Path -Leaf $inputPath
        }

        if ([string]::IsNullOrWhiteSpace($request)) { throw 'A non-empty task request is required.' }
        $request = $request.Trim()
        if ($request.Length -gt [int]$Config.runner.max_task_text_chars) { throw 'Task request exceeds configured limit.' }
        if (-not $requestedWorkspace) { $requestedWorkspace = [string]$Config.repo_root }
        $workspacePath = Resolve-WorkspaceValue $requestedWorkspace

        $taskId = 'aria-' + (Get-Date).ToString('yyyyMMddTHHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)
        $TaskDirectory = Join-Path $TasksRoot $taskId
        New-Item -ItemType Directory -Path $TaskDirectory | Out-Null
        $TaskPath = Join-Path $TaskDirectory 'task.json'
        $CheckpointPath = Join-Path $TaskDirectory 'checkpoint.json'
        $EventsPath = Join-Path $TaskDirectory 'events.jsonl'
        $FinalReportPath = Join-Path $TaskDirectory 'final-report.json'

        $TaskObject = [pscustomobject][ordered]@{
            schema_version = 1
            task_id = $taskId
            task_digest = ''
            created_at = Get-IsoTimestamp
            workspace = $workspacePath
            user_request = $request
            input_source = [pscustomobject][ordered]@{ kind = $inputKind; file_name = $inputFileName }
            scope = [pscustomobject][ordered]@{ requested = if ($null -eq $requestedScope) { $null } else { [string]$requestedScope }; enforced = 'PHASE_2_INTAKE_ONLY' }
            canonical_files = @($CanonicalRelative)
            allowed_paths = @($TaskDirectory)
            forbidden_paths = @(
                (Join-Path $RepoRoot 'electronics'),
                (Join-Path $RepoRoot 'firmware'),
                (Join-Path $RepoRoot 'software'),
                (Join-Path $RepoRoot 'docs\ARIA-MASTER-HANDOFF.md'),
                (Join-Path $RepoRoot 'docs\ARIA-PCB-PRO-MAX-CANONICAL.md'),
                (Join-Path $RepoRoot 'docs\ARIA-BOM-001.md'),
                (Join-Path $RepoRoot 'docs\ARIA-WIRING-001.md')
            )
            required_evidence = @('task_packet_valid', 'canonical_loaded', 'workspace_verified', 'phase_0_pass', 'phase_1_pass', 'c2c_healthy', 'phase_2_boundary_enforced')
            current_stage = 'RECEIVED'
            status = 'RUNNING'
            attempt_count = 1
        }
        $TaskObject.task_digest = Get-TaskDigest $TaskObject
        $CheckpointObject = [pscustomobject][ordered]@{
            schema_version = 1
            task_id = $taskId
            task_digest = $TaskObject.task_digest
            updated_at = Get-IsoTimestamp
            current_stage = 'RECEIVED'
            status = 'RUNNING'
            attempt_count = 1
            completed_stages = @()
            resume_stage = $null
            last_error = $null
            stage_evidence = [pscustomobject][ordered]@{}
        }
    }

    $LockStream = [System.IO.FileStream]::new((Join-Path $TaskDirectory '.runner.lock'), [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    if (Test-Path -LiteralPath $EventsPath) { $script:EventCount = @(Get-Content -LiteralPath $EventsPath).Count }

    if ($PSCmdlet.ParameterSetName -eq 'Resume') {
        $TaskObject = Read-Json $TaskPath
        $CheckpointObject = Read-Json $CheckpointPath
        Assert-TaskPacket $TaskObject
        Assert-Checkpoint -Task $TaskObject -Checkpoint $CheckpointObject

        if ([string]$CheckpointObject.status -eq 'COMPLETED' -and [string]$CheckpointObject.current_stage -eq 'STOP') {
            $existing = Read-Json $FinalReportPath
            $existing | ConvertTo-Json -Depth 20
            return
        }

        $CheckpointObject.attempt_count = [int]$CheckpointObject.attempt_count + 1
        if ([string]$CheckpointObject.status -eq 'FAILED') {
            if (-not $CheckpointObject.resume_stage) { throw 'Failed checkpoint has no resume_stage.' }
            $CheckpointObject.current_stage = [string]$CheckpointObject.resume_stage
        }
        $CheckpointObject.status = 'RUNNING'
        $CheckpointObject.resume_stage = $null
        $CheckpointObject.last_error = $null
        Save-State -Task $TaskObject -Checkpoint $CheckpointObject -TaskPath $TaskPath -CheckpointPath $CheckpointPath
        Add-Event -EventsPath $EventsPath -TaskId $TaskObject.task_id -Attempt $CheckpointObject.attempt_count -Stage $CheckpointObject.current_stage -Event 'RUN_RESUMED' -Message 'Resumed from the durable checkpoint.'
    }
    else {
        Assert-TaskPacket $TaskObject
        Save-State -Task $TaskObject -Checkpoint $CheckpointObject -TaskPath $TaskPath -CheckpointPath $CheckpointPath
        Add-Event -EventsPath $EventsPath -TaskId $TaskObject.task_id -Attempt 1 -Stage 'RECEIVED' -Event 'RUN_CREATED' -Message 'Normalized task packet created.'
    }

    while ([string]$CheckpointObject.current_stage -ne 'STOP') {
        $CurrentStage = [string]$CheckpointObject.current_stage
        Add-Event -EventsPath $EventsPath -TaskId $TaskObject.task_id -Attempt $CheckpointObject.attempt_count -Stage $CurrentStage -Event 'STAGE_STARTED' -Message "Stage $CurrentStage started."

        switch ($CurrentStage) {
            'RECEIVED' {
                Assert-TaskPacket $TaskObject
                $evidence = [pscustomobject][ordered]@{
                    packet_valid = $true
                    input_kind = [string]$TaskObject.input_source.kind
                    request_chars = ([string]$TaskObject.user_request).Length
                    task_digest = [string]$TaskObject.task_digest
                }
                $NextStage = 'CONTEXT_LOAD'
            }
            'CONTEXT_LOAD' {
                if (-not (Test-Path -LiteralPath $CanonicalPath -PathType Leaf)) { throw "Automation canonical not found: $CanonicalPath" }
                if (-not (Test-Path -LiteralPath $PolicyPath -PathType Leaf)) { throw "Repository policy not found: $PolicyPath" }
                $canonicalText = Get-Content -LiteralPath $CanonicalPath -Raw
                $policyText = Get-Content -LiteralPath $PolicyPath -Raw
                $evidence = [pscustomobject][ordered]@{
                    canonical_file = $CanonicalRelative
                    canonical_sha256 = (Get-FileHash -LiteralPath $CanonicalPath -Algorithm SHA256).Hash.ToLowerInvariant()
                    canonical_chars = $canonicalText.Length
                    policy_file = 'AGENTS.md'
                    policy_sha256 = (Get-FileHash -LiteralPath $PolicyPath -Algorithm SHA256).Hash.ToLowerInvariant()
                    policy_chars = $policyText.Length
                    raw_context_copied = $false
                }
                $NextStage = 'PRECHECK'
            }
            'PRECHECK' {
                $workspacePath = Get-NormalizedPath ([string]$TaskObject.workspace)
                if (-not (Test-Path -LiteralPath $workspacePath -PathType Container)) { throw "Workspace does not exist: $workspacePath" }
                $gitRoot = (& git -C $workspacePath rev-parse --show-toplevel 2>$null | Out-String).Trim()
                if ($LASTEXITCODE -ne 0 -or -not $gitRoot) { throw "Workspace is not a Git worktree: $workspacePath" }
                $gitRoot = Get-NormalizedPath $gitRoot
                if (-not $gitRoot.Equals((Get-NormalizedPath $RepoRoot), [StringComparison]::OrdinalIgnoreCase)) { throw "Workspace is not the configured ARIA repository: $gitRoot" }
                if (-not (Test-PathWithin -Candidate $TaskDirectory -Parent $AutomationRoot)) { throw 'Task packet escaped the automation namespace.' }
                $canonicalText = Get-Content -LiteralPath $CanonicalPath -Raw
                if ($canonicalText -notmatch 'Gate: `PHASE_0_PASS`') { throw 'Phase 0 PASS gate is missing.' }
                if ($canonicalText -notmatch 'Gate: `PHASE_1_PASS`') { throw 'Phase 1 PASS gate is missing.' }
                $healthScript = Join-Path $AutomationRoot 'windows\aria-c2c.ps1'
                $healthRaw = (& $healthScript Health | Out-String).Trim()
                $health = $healthRaw | ConvertFrom-Json
                if (-not $health.ready) { throw 'C2C runtime health is not ready.' }
                $evidence = [pscustomobject][ordered]@{
                    workspace_verified = $true
                    workspace = $gitRoot
                    phase_0_pass = $true
                    phase_1_pass = $true
                    c2c_ready = [bool]$health.ready
                    c2c_local_port = [int]$health.local_port
                    c2c_tunnel_http_status = [int]$health.tunnel_http_status
                    allowed_write_root = [string]$TaskObject.allowed_paths[0]
                    forbidden_path_count = @($TaskObject.forbidden_paths).Count
                }
                $NextStage = 'READY_FOR_ROUTING'
            }
            'READY_FOR_ROUTING' {
                $evidence = [pscustomobject][ordered]@{
                    packet_ready_for_future_router = $true
                    routing_started = $false
                    council_started = $false
                    codex_execution_started = $false
                    repository_execution_started = $false
                }
                $NextStage = 'STOP'
            }
            default { throw "Unsupported stage: $CurrentStage" }
        }

        Set-StageEvidence -Checkpoint $CheckpointObject -Stage $CurrentStage -Evidence $evidence
        Add-CompletedStage -Checkpoint $CheckpointObject -Stage $CurrentStage
        $CheckpointObject.current_stage = $NextStage
        $CheckpointObject.status = if ($NextStage -eq 'STOP') { 'COMPLETED' } else { 'RUNNING' }
        Save-State -Task $TaskObject -Checkpoint $CheckpointObject -TaskPath $TaskPath -CheckpointPath $CheckpointPath
        Add-Event -EventsPath $EventsPath -TaskId $TaskObject.task_id -Attempt $CheckpointObject.attempt_count -Stage $CurrentStage -Event 'STAGE_PASSED' -Message "Stage $CurrentStage passed." -Evidence ([ordered]@{ next_stage = $NextStage })

        if ($StopAfterStage -and $StopAfterStage -eq $CurrentStage -and $NextStage -ne 'STOP') {
            $CheckpointObject.status = 'INTERRUPTED'
            Save-State -Task $TaskObject -Checkpoint $CheckpointObject -TaskPath $TaskPath -CheckpointPath $CheckpointPath
            Add-Event -EventsPath $EventsPath -TaskId $TaskObject.task_id -Attempt $CheckpointObject.attempt_count -Stage $CheckpointObject.current_stage -Event 'RUN_INTERRUPTED' -Message 'Controlled interruption recorded; resume is available.'
            break
        }
    }

    if ([string]$CheckpointObject.current_stage -eq 'STOP' -and [string]$CheckpointObject.status -eq 'COMPLETED') {
        Add-Event -EventsPath $EventsPath -TaskId $TaskObject.task_id -Attempt $CheckpointObject.attempt_count -Stage 'STOP' -Event 'RUN_STOPPED' -Message 'Phase 2 boundary reached; no routing or execution was started.'
    }

    $report = New-FinalReport -Task $TaskObject -Checkpoint $CheckpointObject -EventsCount $script:EventCount
    Write-JsonAtomic -Path $FinalReportPath -Value $report
    $report | ConvertTo-Json -Depth 20
}
catch {
    $message = $_.Exception.Message
    if ($null -ne $TaskObject -and $null -ne $CheckpointObject -and $TaskPath -and $CheckpointPath) {
        $failureStage = if ($CurrentStage -and $CurrentStage -ne 'STOP') { $CurrentStage } else { [string]$CheckpointObject.current_stage }
        if ($failureStage -eq 'STOP' -and $CheckpointObject.resume_stage) { $failureStage = [string]$CheckpointObject.resume_stage }
        $CheckpointObject.status = 'FAILED'
        $CheckpointObject.current_stage = 'STOP'
        $CheckpointObject.resume_stage = $failureStage
        $CheckpointObject.last_error = [pscustomobject][ordered]@{ stage = $failureStage; message = $message; timestamp = Get-IsoTimestamp }
        Save-State -Task $TaskObject -Checkpoint $CheckpointObject -TaskPath $TaskPath -CheckpointPath $CheckpointPath
        try { Add-Event -EventsPath $EventsPath -TaskId $TaskObject.task_id -Attempt $CheckpointObject.attempt_count -Stage $failureStage -Event 'STAGE_FAILED' -Message $message } catch {}
        $report = New-FinalReport -Task $TaskObject -Checkpoint $CheckpointObject -EventsCount $script:EventCount
        Write-JsonAtomic -Path $FinalReportPath -Value $report
        $report | ConvertTo-Json -Depth 20
    }
    else {
        [ordered]@{ schema_version = 1; status = 'FAILED'; result = 'FAILED_BEFORE_PACKET'; error = $message } | ConvertTo-Json -Depth 6
    }
    exit 2
}
finally {
    if ($null -ne $LockStream) { $LockStream.Dispose() }
}
