[CmdletBinding()]
param(
    [ValidateSet('Status', 'Health', 'Ensure')]
    [string]$Action = 'Status'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ConfigPath = Join-Path $RepoRoot 'automation\config.json'
$Config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
$StateRoot = [Environment]::ExpandEnvironmentVariables([string]$Config.state_root)
$C2CRoot = [Environment]::ExpandEnvironmentVariables([string]$Config.c2c.root)
$UpstreamConfigPath = Join-Path $C2CRoot 'config.json'

function Get-CommandLineProcesses {
    param([string]$Needle)
    @(Get-CimInstance Win32_Process | Where-Object {
        $_.CommandLine -and $_.CommandLine.IndexOf($Needle, [StringComparison]::OrdinalIgnoreCase) -ge 0
    })
}

function Test-TcpEndpoint {
    param([string]$HostName, [int]$Port, [int]$TimeoutMs = 1000)
    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $async = $client.BeginConnect($HostName, $Port, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) { return $false }
        $client.EndConnect($async)
        return $true
    }
    catch { return $false }
    finally { $client.Dispose() }
}

function Get-C2CContext {
    if (-not (Test-Path -LiteralPath $UpstreamConfigPath)) {
        throw "C2C config not found: $UpstreamConfigPath"
    }

    $up = Get-Content -LiteralPath $UpstreamConfigPath -Raw | ConvertFrom-Json
    if (-not $up.runtimeCommand -or $up.runtimeCommand.Count -lt 2) {
        throw 'C2C runtimeCommand is missing or incomplete.'
    }

    $profile = [string]$up.tunnel.profileName
    [pscustomobject]@{
        Upstream = $up
        RuntimeExe = [string]$up.runtimeCommand[0]
        CliPath = [string]$up.runtimeCommand[1]
        Host = [string]$up.host
        Port = [int]$up.port
        TunnelExe = [string]$up.tunnel.binaryPath
        TunnelProfileDir = [string]$up.tunnel.profileDir
        TunnelProfile = $profile
        TunnelHealthFile = Join-Path $env:USERPROFILE ".local\state\tunnel-client\health\$profile.url"
    }
}

function Get-C2CHealth {
    param($Context)

    $cli = $Context.CliPath
    $serve = Get-CommandLineProcesses $cli | Where-Object { $_.CommandLine -match '(?i)(^|\s)serve(\s|$)' }
    $mcp = Get-CommandLineProcesses $cli | Where-Object { $_.CommandLine -match '(?i)(^|\s)mcp(\s|$)' }
    $tunnel = Get-CommandLineProcesses $Context.TunnelExe | Where-Object {
        $_.CommandLine -match '(?i)(^|\s)run(\s|$)' -and $_.CommandLine.IndexOf($Context.TunnelProfile, [StringComparison]::OrdinalIgnoreCase) -ge 0
    }

    $portOk = Test-TcpEndpoint -HostName $Context.Host -Port $Context.Port
    $tunnelUrl = $null
    $tunnelHttp = $null
    if (Test-Path -LiteralPath $Context.TunnelHealthFile) {
        $tunnelUrl = (Get-Content -LiteralPath $Context.TunnelHealthFile -Raw).Trim()
        if ($tunnelUrl) {
            try {
                $resp = Invoke-WebRequest -UseBasicParsing -Uri $tunnelUrl -TimeoutSec ([int]$Config.c2c.health_timeout_sec)
                $tunnelHttp = [int]$resp.StatusCode
            }
            catch { $tunnelHttp = 0 }
        }
    }

    $appNameOk = ([string]$Context.Upstream.appName -eq [string]$Config.c2c.expected_app_name)
    $ready = (@($serve).Count -gt 0) -and $portOk -and (@($tunnel).Count -gt 0) -and ($tunnelHttp -eq 200) -and (@($mcp).Count -gt 0) -and $appNameOk

    [pscustomobject]@{
        schema = 1
        timestamp = (Get-Date).ToString('o')
        ready = [bool]$ready
        app_name = [string]$Context.Upstream.appName
        app_name_ok = [bool]$appNameOk
        release_version = [string]$Context.Upstream.releaseVersion
        serve_process_count = @($serve).Count
        local_host = $Context.Host
        local_port = $Context.Port
        local_port_ok = [bool]$portOk
        tunnel_process_count = @($tunnel).Count
        tunnel_health_url_present = [bool]$tunnelUrl
        tunnel_http_status = $tunnelHttp
        mcp_process_count = @($mcp).Count
    }
}

function Save-C2CHealth {
    param($Health)
    New-Item -ItemType Directory -Force -Path $StateRoot | Out-Null
    $healthPath = Join-Path $StateRoot 'c2c-health.json'
    $tempPath = "$healthPath.tmp"
    $Health | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $tempPath -Encoding UTF8
    Move-Item -LiteralPath $tempPath -Destination $healthPath -Force
}

function Start-C2CServerIfMissing {
    param($Context, $Health)
    if ($Health.serve_process_count -gt 0 -and $Health.local_port_ok) { return }
    if (-not (Test-Path -LiteralPath $Context.RuntimeExe)) { throw "C2C runtime missing: $($Context.RuntimeExe)" }
    if (-not (Test-Path -LiteralPath $Context.CliPath)) { throw "C2C CLI missing: $($Context.CliPath)" }
    Start-Process -FilePath $Context.RuntimeExe -ArgumentList @($Context.CliPath, 'serve') -WindowStyle Hidden | Out-Null
}

function Start-C2CTunnelIfMissing {
    param($Context, $Health)
    if ($Health.tunnel_process_count -gt 0) { return }
    if (-not (Test-Path -LiteralPath $Context.TunnelExe)) { throw "C2C tunnel client missing: $($Context.TunnelExe)" }
    Start-Process -FilePath $Context.TunnelExe -ArgumentList @('run', '--profile-dir', $Context.TunnelProfileDir, '--profile', $Context.TunnelProfile) -WindowStyle Hidden | Out-Null
}

$ctx = Get-C2CContext
$health = Get-C2CHealth -Context $ctx

if ($Action -eq 'Ensure') {
    Start-C2CServerIfMissing -Context $ctx -Health $health
    Start-C2CTunnelIfMissing -Context $ctx -Health $health

    $deadline = (Get-Date).AddSeconds([int]$Config.c2c.start_timeout_sec)
    do {
        Start-Sleep -Milliseconds 500
        $health = Get-C2CHealth -Context $ctx
        if ($health.ready) { break }
    } while ((Get-Date) -lt $deadline)
}

Save-C2CHealth -Health $health
$health | ConvertTo-Json -Depth 6

if ($Action -in @('Health', 'Ensure') -and -not $health.ready) { exit 2 }
