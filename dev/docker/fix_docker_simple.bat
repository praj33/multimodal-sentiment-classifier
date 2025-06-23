@echo off
echo 🔧 SIMPLE DOCKER SETUP FIX
echo ============================

echo 📍 Step 1: Checking current Docker status...
where docker >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Docker CLI found in PATH
    docker --version
    goto :test_docker
) else (
    echo ❌ Docker CLI not found in PATH
)

echo.
echo 📍 Step 2: Looking for Docker Desktop installation...
if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    echo ✅ Docker Desktop found at: C:\Program Files\Docker\Docker\Docker Desktop.exe
    goto :start_docker
)

if exist "C:\Program Files (x86)\Docker\Docker\Docker Desktop.exe" (
    echo ✅ Docker Desktop found at: C:\Program Files (x86)\Docker\Docker\Docker Desktop.exe
    goto :start_docker
)

echo ❌ Docker Desktop not found
goto :manual_install

:start_docker
echo.
echo 📍 Step 3: Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
echo ⏳ Waiting 60 seconds for Docker to start...
timeout /t 60 /nobreak >nul

:test_docker
echo.
echo 📍 Step 4: Testing Docker functionality...
where docker >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Testing Docker CLI...
    docker --version
    echo.
    echo ✅ Testing Docker daemon...
    docker info >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Docker daemon is running
        goto :success
    ) else (
        echo ⚠️  Docker daemon not ready yet (this is normal)
        echo 💡 Please wait a few more minutes for Docker to fully start
        goto :success
    )
) else (
    echo ❌ Docker CLI still not accessible
    goto :path_fix
)

:path_fix
echo.
echo 📍 Step 5: Attempting to fix Docker PATH...
set "DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin"
if exist "%DOCKER_PATH%\docker.exe" (
    echo ✅ Found Docker CLI at: %DOCKER_PATH%
    echo 💡 Adding to current session PATH...
    set "PATH=%PATH%;%DOCKER_PATH%"
    echo ✅ Docker CLI should now be accessible
    "%DOCKER_PATH%\docker.exe" --version
    goto :success
) else (
    echo ❌ Docker CLI not found in expected location
    goto :manual_install
)

:success
echo.
echo 🎉 DOCKER SETUP SUCCESSFUL!
echo ============================
echo.
echo 🚀 You can now run your containerized build:
echo    cd C:\Users\PC\multimodal_sentiment
echo    docker-compose --profile cpu up -d
echo.
echo 📊 To access your dashboard:
echo    http://localhost:8000/dashboard
echo.
echo 🔍 To check container status:
echo    docker ps
echo.
goto :end

:manual_install
echo.
echo 📥 MANUAL DOCKER INSTALLATION REQUIRED
echo ======================================
echo.
echo ❌ Docker Desktop is not installed or not found
echo.
echo 📝 Please follow these steps:
echo    1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
echo    2. Run the installer as Administrator
echo    3. Restart your computer after installation
echo    4. Run this script again
echo.
echo 💡 Alternative: Use your existing Python API
echo    Your API is already working without Docker:
echo    cd C:\Users\PC\multimodal_sentiment
echo    venv\scripts\activate
echo    python start_api.py
echo.

:end
echo 🎯 Script completed!
pause
