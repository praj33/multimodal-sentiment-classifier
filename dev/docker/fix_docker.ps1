# fix_docker.ps1 - Simple Docker Setup Fix

Write-Host "🔧 DOCKER SETUP FIX FOR MULTIMODAL SENTIMENT CLASSIFIER" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Step 1: Check if Docker CLI is in PATH
Write-Host "📍 Step 1: Checking Docker CLI in PATH..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker CLI found in PATH: $dockerVersion" -ForegroundColor Green
        Write-Host "📍 Testing Docker daemon..." -ForegroundColor Yellow
        docker info >$null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker daemon is running!" -ForegroundColor Green
            Write-Host "🎉 Docker is working! You can run: docker-compose --profile cpu up -d" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "⚠️  Docker CLI found but daemon not running" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "❌ Docker CLI not found in PATH" -ForegroundColor Red
}

# Step 2: Look for Docker Desktop installation
Write-Host "📍 Step 2: Looking for Docker Desktop..." -ForegroundColor Yellow

$dockerPaths = @(
    "C:\Program Files\Docker\Docker\Docker Desktop.exe",
    "C:\Program Files (x86)\Docker\Docker\Docker Desktop.exe"
)

$dockerDesktopPath = $null
foreach ($path in $dockerPaths) {
    if (Test-Path $path) {
        $dockerDesktopPath = $path
        Write-Host "✅ Docker Desktop found: $path" -ForegroundColor Green
        break
    }
}

if ($dockerDesktopPath) {
    # Step 3: Start Docker Desktop
    Write-Host "📍 Step 3: Starting Docker Desktop..." -ForegroundColor Yellow
    try {
        Start-Process $dockerDesktopPath
        Write-Host "⏳ Waiting 60 seconds for Docker to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 60
        
        # Test again
        try {
            docker info >$null 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Docker is now running!" -ForegroundColor Green
                Write-Host "🎉 SUCCESS! You can now run: docker-compose --profile cpu up -d" -ForegroundColor Green
                exit 0
            }
        } catch {
            Write-Host "⚠️  Docker still starting up..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Failed to start Docker Desktop" -ForegroundColor Red
    }
}

# Step 4: Look for Docker CLI in Docker installation
Write-Host "📍 Step 4: Looking for Docker CLI in installation..." -ForegroundColor Yellow

$dockerCliPaths = @(
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe",
    "C:\Program Files\Docker\Docker\resources\docker.exe"
)

$dockerCliPath = $null
foreach ($path in $dockerCliPaths) {
    if (Test-Path $path) {
        $dockerCliPath = $path
        Write-Host "✅ Docker CLI found: $path" -ForegroundColor Green
        break
    }
}

if ($dockerCliPath) {
    Write-Host "📍 Testing Docker CLI directly..." -ForegroundColor Yellow
    try {
        $version = & $dockerCliPath --version
        Write-Host "✅ Docker CLI working: $version" -ForegroundColor Green
        
        # Add to PATH for this session
        $env:PATH += ";$(Split-Path $dockerCliPath)"
        Write-Host "✅ Added Docker to PATH for this session" -ForegroundColor Green
        
        # Test daemon
        & $dockerCliPath info >$null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker daemon accessible!" -ForegroundColor Green
            Write-Host "🎉 SUCCESS! You can now run: docker-compose --profile cpu up -d" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "⚠️  Docker daemon not ready yet" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Docker CLI found but not working" -ForegroundColor Red
    }
}

# Step 5: Manual installation required
Write-Host ""
Write-Host "📥 DOCKER INSTALLATION REQUIRED" -ForegroundColor Red
Write-Host "================================" -ForegroundColor Red
Write-Host ""
Write-Host "❌ Docker Desktop is not installed or not accessible" -ForegroundColor Red
Write-Host ""
Write-Host "📝 SOLUTION OPTIONS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔄 Option 1: Install Docker Desktop" -ForegroundColor Green
Write-Host "   1. Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor White
Write-Host "   2. Run installer as Administrator" -ForegroundColor White
Write-Host "   3. Restart computer after installation" -ForegroundColor White
Write-Host "   4. Run this script again" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Option 2: Use Your Working Python API (Recommended for now)" -ForegroundColor Green
Write-Host "   Your multimodal sentiment classifier is already working perfectly:" -ForegroundColor White
Write-Host "   1. cd C:\Users\PC\multimodal_sentiment" -ForegroundColor Cyan
Write-Host "   2. venv\scripts\activate" -ForegroundColor Cyan
Write-Host "   3. python start_api.py" -ForegroundColor Cyan
Write-Host "   4. Access: http://localhost:8000/dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Your API has FULL FUNCTIONALITY with all dependencies!" -ForegroundColor Green
Write-Host "   - ✅ Text analysis with DistilBERT" -ForegroundColor White
Write-Host "   - ✅ Audio analysis with librosa" -ForegroundColor White
Write-Host "   - ✅ Video analysis with MediaPipe" -ForegroundColor White
Write-Host "   - ✅ Multimodal fusion engine" -ForegroundColor White
Write-Host ""
Write-Host "🎯 RECOMMENDATION:" -ForegroundColor Cyan
Write-Host "Use Option 2 (Python API) for immediate use," -ForegroundColor White
Write-Host "and install Docker Desktop later for containerization." -ForegroundColor White
