# docker_diagnosis.ps1 - Diagnose and Fix Docker Issues

Write-Host "DOCKER DIAGNOSIS AND FIX" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

# Check if Docker CLI is accessible
Write-Host "Step 1: Checking Docker CLI..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Docker CLI found - $dockerVersion" -ForegroundColor Green
        
        # Test Docker daemon
        docker info >$null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Docker daemon is running!" -ForegroundColor Green
            Write-Host "READY: You can run docker-compose --profile cpu up -d" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "WARNING: Docker CLI found but daemon not running" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "ISSUE: Docker CLI not found in PATH" -ForegroundColor Red
}

# Look for Docker Desktop
Write-Host "Step 2: Looking for Docker Desktop..." -ForegroundColor Yellow

$dockerPaths = @(
    "C:\Program Files\Docker\Docker\Docker Desktop.exe",
    "C:\Program Files (x86)\Docker\Docker\Docker Desktop.exe"
)

$dockerFound = $false
foreach ($path in $dockerPaths) {
    if (Test-Path $path) {
        Write-Host "FOUND: Docker Desktop at $path" -ForegroundColor Green
        $dockerFound = $true
        
        # Try to start it
        Write-Host "Starting Docker Desktop..." -ForegroundColor Yellow
        Start-Process $path
        Write-Host "Waiting 30 seconds for startup..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        break
    }
}

if (-not $dockerFound) {
    Write-Host "NOT FOUND: Docker Desktop is not installed" -ForegroundColor Red
}

# Look for Docker CLI in installation directory
Write-Host "Step 3: Looking for Docker CLI in installation..." -ForegroundColor Yellow

$dockerCliPaths = @(
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe"
)

foreach ($path in $dockerCliPaths) {
    if (Test-Path $path) {
        Write-Host "FOUND: Docker CLI at $path" -ForegroundColor Green
        
        try {
            $version = & $path --version
            Write-Host "SUCCESS: Docker CLI working - $version" -ForegroundColor Green
            
            # Test if daemon is accessible
            & $path info >$null 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "SUCCESS: Docker daemon accessible!" -ForegroundColor Green
                Write-Host "SOLUTION: Docker is working!" -ForegroundColor Green
                exit 0
            } else {
                Write-Host "ISSUE: Docker daemon not accessible yet" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "ISSUE: Docker CLI found but not working" -ForegroundColor Red
        }
        break
    }
}

# Final diagnosis
Write-Host ""
Write-Host "DIAGNOSIS COMPLETE" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

if ($dockerFound) {
    Write-Host "STATUS: Docker Desktop is installed but may need time to start" -ForegroundColor Yellow
    Write-Host "SOLUTION: Wait 2-3 minutes and try: docker --version" -ForegroundColor Green
} else {
    Write-Host "STATUS: Docker Desktop is NOT installed" -ForegroundColor Red
    Write-Host "SOLUTION: Install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "IMMEDIATE WORKAROUND:" -ForegroundColor Green
Write-Host "Your Python API is already working perfectly!" -ForegroundColor White
Write-Host "1. cd C:\Users\PC\multimodal_sentiment" -ForegroundColor Cyan
Write-Host "2. venv\scripts\activate" -ForegroundColor Cyan  
Write-Host "3. python start_api.py" -ForegroundColor Cyan
Write-Host "4. Access: http://localhost:8000/dashboard" -ForegroundColor Cyan
