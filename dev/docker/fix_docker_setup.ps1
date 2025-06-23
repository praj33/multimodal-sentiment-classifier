# fix_docker_setup.ps1 - Fix Docker Desktop Installation and Setup

Write-Host "🔧 FIXING DOCKER SETUP FOR MULTIMODAL SENTIMENT CLASSIFIER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  This script needs to run as Administrator to install Docker Desktop" -ForegroundColor Yellow
    Write-Host "📝 Please run PowerShell as Administrator and try again" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🔄 Alternative: Manual Docker Desktop Installation" -ForegroundColor Green
    Write-Host "1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor White
    Write-Host "2. Run the installer as Administrator" -ForegroundColor White
    Write-Host "3. Restart your computer after installation" -ForegroundColor White
    Write-Host "4. Run this script again to verify setup" -ForegroundColor White
    exit 1
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green

# Check if Docker Desktop is already installed
Write-Host "🔍 Checking Docker Desktop installation..." -ForegroundColor Yellow

$dockerPaths = @(
    "C:\Program Files\Docker\Docker\Docker Desktop.exe",
    "C:\Program Files (x86)\Docker\Docker\Docker Desktop.exe"
)

$dockerInstalled = $false
foreach ($path in $dockerPaths) {
    if (Test-Path $path) {
        Write-Host "✅ Docker Desktop found at: $path" -ForegroundColor Green
        $dockerInstalled = $true
        break
    }
}

if (-not $dockerInstalled) {
    Write-Host "❌ Docker Desktop not found" -ForegroundColor Red
    Write-Host "📥 Downloading Docker Desktop..." -ForegroundColor Yellow
    
    # Download Docker Desktop
    $dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    $dockerInstaller = "$env:TEMP\DockerDesktopInstaller.exe"
    
    try {
        Invoke-WebRequest -Uri $dockerUrl -OutFile $dockerInstaller -UseBasicParsing
        Write-Host "✅ Docker Desktop downloaded" -ForegroundColor Green
        
        Write-Host "🚀 Installing Docker Desktop..." -ForegroundColor Yellow
        Start-Process -FilePath $dockerInstaller -ArgumentList "install", "--quiet" -Wait
        
        Write-Host "✅ Docker Desktop installation completed" -ForegroundColor Green
        Write-Host "🔄 Please restart your computer and run this script again" -ForegroundColor Yellow
        exit 0
        
    } catch {
        Write-Host "❌ Failed to download/install Docker Desktop: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "📝 Please manually download and install from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        exit 1
    }
}

# Check if Docker service is running
Write-Host "🔍 Checking Docker service status..." -ForegroundColor Yellow

try {
    $dockerService = Get-Service -Name "com.docker.service" -ErrorAction SilentlyContinue
    if ($dockerService -and $dockerService.Status -eq "Running") {
        Write-Host "✅ Docker service is running" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Docker service not running, starting Docker Desktop..." -ForegroundColor Yellow
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        Write-Host "⏳ Waiting for Docker Desktop to start (60 seconds)..." -ForegroundColor Yellow
        Start-Sleep -Seconds 60
    }
} catch {
    Write-Host "⚠️  Could not check Docker service, attempting to start Docker Desktop..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 60
}

# Verify Docker CLI is accessible
Write-Host "🔍 Verifying Docker CLI..." -ForegroundColor Yellow

$dockerCliPaths = @(
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe",
    "C:\Program Files\Docker\Docker\resources\docker.exe"
)

$dockerCli = $null
foreach ($path in $dockerCliPaths) {
    if (Test-Path $path) {
        $dockerCli = $path
        break
    }
}

if ($dockerCli) {
    Write-Host "✅ Docker CLI found at: $dockerCli" -ForegroundColor Green
    
    # Test Docker
    try {
        $dockerVersion = & $dockerCli --version
        Write-Host "✅ Docker version: $dockerVersion" -ForegroundColor Green
        
        # Test Docker info
        $dockerInfo = & $dockerCli info 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker daemon is accessible" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Docker daemon not ready yet, this is normal on first startup" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "⚠️  Docker CLI found but not responding yet" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Docker CLI not found in expected locations" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 DOCKER SETUP STATUS:" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

if ($dockerInstalled) {
    Write-Host "✅ Docker Desktop: Installed" -ForegroundColor Green
} else {
    Write-Host "❌ Docker Desktop: Not Installed" -ForegroundColor Red
}

if ($dockerCli) {
    Write-Host "✅ Docker CLI: Available" -ForegroundColor Green
} else {
    Write-Host "❌ Docker CLI: Not Found" -ForegroundColor Red
}

Write-Host ""
Write-Host "🚀 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan

if ($dockerInstalled -and $dockerCli) {
    Write-Host "1. Wait for Docker Desktop to fully start (may take 2-3 minutes)" -ForegroundColor White
    Write-Host "2. Open a new PowerShell window" -ForegroundColor White
    Write-Host "3. Navigate to your project: cd C:\Users\PC\multimodal_sentiment" -ForegroundColor White
    Write-Host "4. Test Docker: docker --version" -ForegroundColor White
    Write-Host "5. Run your containerized build: docker-compose --profile cpu up -d" -ForegroundColor White
} else {
    Write-Host "1. Install Docker Desktop manually from: https://www.docker.com/products/docker-desktop" -ForegroundColor White
    Write-Host "2. Restart your computer after installation" -ForegroundColor White
    Write-Host "3. Run this script again to verify setup" -ForegroundColor White
}

Write-Host ""
Write-Host "🎉 Docker setup script completed!" -ForegroundColor Green
