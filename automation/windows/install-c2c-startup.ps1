[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Config = Get-Content -LiteralPath (Join-Path $RepoRoot 'automation\config.json') -Raw | ConvertFrom-Json
$Manager = Join-Path $PSScriptRoot 'aria-c2c.ps1'
$PowerShellExe = Join-Path $PSHOME 'powershell.exe'
if (-not (Test-Path -LiteralPath $PowerShellExe)) { $PowerShellExe = 'powershell.exe' }

$taskArgs = "-NoProfile -ExecutionPolicy Bypass -File `"$Manager`" Ensure"
$action = New-ScheduledTaskAction -Execute $PowerShellExe -Argument $taskArgs -WorkingDirectory $RepoRoot
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries -MultipleInstances IgnoreNew -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited

$startupName = [string]$Config.windows.startup_task
$watchdogName = [string]$Config.windows.watchdog_task
$startupTrigger = New-ScheduledTaskTrigger -AtLogOn -User ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)
$watchdogTrigger = New-ScheduledTaskTrigger -Once -At ((Get-Date).AddMinutes(1)) -RepetitionInterval (New-TimeSpan -Minutes ([int]$Config.windows.watchdog_minutes)) -RepetitionDuration (New-TimeSpan -Days 3650)

Register-ScheduledTask -TaskName $startupName -Action $action -Trigger $startupTrigger -Settings $settings -Principal $principal -Force | Out-Null
Register-ScheduledTask -TaskName $watchdogName -Action $action -Trigger $watchdogTrigger -Settings $settings -Principal $principal -Force | Out-Null

Get-ScheduledTask -TaskName $startupName, $watchdogName | Select-Object TaskName, State, TaskPath
