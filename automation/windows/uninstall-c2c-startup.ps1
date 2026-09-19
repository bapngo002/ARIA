[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Config = Get-Content -LiteralPath (Join-Path $RepoRoot 'automation\config.json') -Raw | ConvertFrom-Json

foreach ($name in @([string]$Config.windows.startup_task, [string]$Config.windows.watchdog_task)) {
    if (Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $name -Confirm:$false
    }
}
