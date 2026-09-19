[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Config = Get-Content -LiteralPath (Join-Path $RepoRoot 'automation\config.json') -Raw | ConvertFrom-Json
$Manager = Join-Path $RepoRoot 'automation\windows\aria-c2c.ps1'

$json = & $Manager Ensure
if (-not $?) { throw 'C2C Ensure failed.' }
$health = $json | ConvertFrom-Json
if (-not $health.ready) { throw 'C2C health is not ready.' }
if (-not $health.app_name_ok) { throw "Unexpected C2C app name: $($health.app_name)" }

$startup = Get-ScheduledTask -TaskName ([string]$Config.windows.startup_task) -ErrorAction Stop
$watchdog = Get-ScheduledTask -TaskName ([string]$Config.windows.watchdog_task) -ErrorAction Stop
if ($startup.Actions.Arguments -notlike "*$Manager*") { throw 'Startup task does not target the canonical manager.' }
if ($watchdog.Actions.Arguments -notlike "*$Manager*") { throw 'Watchdog task does not target the canonical manager.' }
if (-not $startup.Settings.Enabled -or -not $watchdog.Settings.Enabled) { throw 'One or more C2C scheduled tasks are disabled.' }
if ($startup.Settings.RestartCount -lt 1 -or $watchdog.Settings.RestartCount -lt 1) { throw 'Scheduled-task restart policy is missing.' }

[pscustomobject]@{
    gate = 'PHASE_1_PASS'
    timestamp = (Get-Date).ToString('o')
    c2c_ready = $health.ready
    release_version = $health.release_version
    local_port = $health.local_port
    tunnel_http_status = $health.tunnel_http_status
    mcp_process_count = $health.mcp_process_count
    startup_task = $startup.TaskName
    watchdog_task = $watchdog.TaskName
    reboot_runtime_evidence = 'PENDING_FIRST_REBOOT_LOGON'
} | ConvertTo-Json -Depth 4
