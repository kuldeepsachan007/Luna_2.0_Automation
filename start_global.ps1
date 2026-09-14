# ============================================================
#  Luna Global Launcher
#  Ek shot me: backend on karta hai -> cloudflared tunnel start
#  karta hai -> tunnel URL nikaalta hai -> dashboard browser me
#  khud khol deta hai (Vercel + ?api, aur direct tunnel URL bhi).
#  Chalane ke liye: start_global.bat par double-click.
# ============================================================
$ErrorActionPreference = "SilentlyContinue"
$root   = $PSScriptRoot
$vercel = "https://luna-2-0-dashboard.vercel.app"   # apni Vercel URL (badle to yahan change)

function PortUp([int]$p) {
  try { $c = New-Object Net.Sockets.TcpClient; $c.Connect("127.0.0.1", $p); $c.Close(); return $true }
  catch { return $false }
}

Write-Host "============ Luna Global Launcher ============" -ForegroundColor Cyan


# 1) BACKEND

if (PortUp 5000) {
  Write-Host "[1/3] Backend pehle se ON hai (127.0.0.1:5000)" -ForegroundColor Green
} else {
  Write-Host "[1/3] Backend start ho raha hai... (ek nayi window khulegi)" -ForegroundColor Yellow
  Start-Process cmd.exe -ArgumentList "/k", "`"$root\dashboard\run_dashboard.bat`""
  $ok = $false
  for ($i = 0; $i -lt 40; $i++) { Start-Sleep 1; if (PortUp 5000) { $ok = $true; break } }
  if (-not $ok) { Write-Host "  Backend start nahi hua. dashboard\run_dashboard.bat khud chalao." -ForegroundColor Red; Read-Host "Enter dabao band karne ke liye"; exit }
  Write-Host "      Backend ready." -ForegroundColor Green
}

# 2) TUNNEL
$cf = Join-Path $root "cloudflared.exe"
if (-not (Test-Path $cf)) {
  Write-Host "  cloudflared.exe is folder me nahi mila. Download karo:" -ForegroundColor Red
  Write-Host '  Invoke-WebRequest "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "cloudflared.exe"'
  Read-Host "Enter"; exit
}
$outLog = Join-Path $root "tunnel.out.log"
$errLog = Join-Path $root "tunnel.err.log"
Remove-Item $outLog, $errLog -ErrorAction SilentlyContinue
Write-Host "[2/3] Tunnel start ho raha hai..." -ForegroundColor Yellow
$proc = Start-Process -FilePath $cf -ArgumentList "tunnel", "--url", "http://localhost:5000" `
        -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru -WindowStyle Hidden

$tunnelUrl = $null
for ($i = 0; $i -lt 45; $i++) {
  Start-Sleep 1
  $txt = Get-Content $outLog, $errLog -ErrorAction SilentlyContinue
  $hit = $txt | Select-String -Pattern "https://[a-z0-9\-]+\.trycloudflare\.com" | Select-Object -First 1
  if ($hit) { $tunnelUrl = $hit.Matches[0].Value; break }
}
if (-not $tunnelUrl) { Write-Host "  Tunnel URL nahi mila. tunnel.err.log dekho." -ForegroundColor Red; Read-Host "Enter"; exit }
Write-Host "      Tunnel ready: $tunnelUrl" -ForegroundColor Green

# 3) BROWSER
$full = "$vercel/?api=$tunnelUrl"
Start-Process $full

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " SAB READY! Dashboard browser me khul gaya." -ForegroundColor Green
Write-Host ""
Write-Host " Vercel (share karne ke liye):" -ForegroundColor Cyan
Write-Host "   $full"
Write-Host " Direct (sabse simple, Vercel ke bina):" -ForegroundColor Cyan
Write-Host "   $tunnelUrl"
Write-Host ""
Write-Host " Is window ko BAND MAT karo (tunnel yahin chal raha hai)." -ForegroundColor Yellow
Write-Host " Rokne ke liye is window me Ctrl+C dabao." -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Green

try { Wait-Process -Id $proc.Id } finally { Stop-Process -Id $proc.Id -ErrorAction SilentlyContinue }
