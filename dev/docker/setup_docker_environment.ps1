# Docker Environment Setup Script for Multimodal Sentiment Analysis
# This script sets up Docker Desktop and validates the containerized deployment

Write-Host "=== Multimodal Sentiment Analysis - Docker Setup ===" -ForegroundColor Green

# Function to check if Docker is installed
function Test-DockerInstalled {
    try {
        $dockerVersion = docker --version 2>$null
        if ($dockerVersion) {
            Write-Host "Docker is installed: $dockerVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "Docker is not installed or not in PATH" -ForegroundColor Yellow
        return $false
    }
    return $false
}

# Function to check if Docker Desktop is running
function Test-DockerRunning {
    try {
        docker info 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Docker Desktop is running" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "Docker Desktop is not running" -ForegroundColor Yellow
        return $false
    }
    return $false
}

# Function to download and install Docker Desktop
function Install-DockerDesktop {
    Write-Host "Downloading Docker Desktop for Windows..." -ForegroundColor Yellow
    
    $dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    $installerPath = "$env:TEMP\DockerDesktopInstaller.exe"
    
    try {
        Invoke-WebRequest -Uri $dockerUrl -OutFile $installerPath -UseBasicParsing
        Write-Host "Docker Desktop downloaded successfully" -ForegroundColor Green
        
        Write-Host "Installing Docker Desktop..." -ForegroundColor Yellow
        Start-Process -FilePath $installerPath -ArgumentList "install", "--quiet" -Wait
        
        Write-Host "Docker Desktop installation completed" -ForegroundColor Green
        Write-Host "Please restart your computer and run this script again" -ForegroundColor Yellow
        
        # Clean up installer
        Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
        
        return $true
    }
    catch {
        Write-Host "Failed to download or install Docker Desktop: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to build Docker images
function Build-DockerImages {
    Write-Host "Building Docker images..." -ForegroundColor Yellow
    
    # Build CPU version
    Write-Host "Building CPU version..." -ForegroundColor Cyan
    docker build --target production -t multimodal-sentiment:cpu .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to build CPU image" -ForegroundColor Red
        return $false
    }
    
    # Build GPU version
    Write-Host "Building GPU version..." -ForegroundColor Cyan
    docker build --target gpu -t multimodal-sentiment:gpu .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to build GPU image" -ForegroundColor Red
        return $false
    }
    
    Write-Host "Docker images built successfully" -ForegroundColor Green
    return $true
}

# Function to test Docker deployment
function Test-DockerDeployment {
    Write-Host "Testing Docker deployment..." -ForegroundColor Yellow
    
    # Test CPU deployment
    Write-Host "Testing CPU deployment..." -ForegroundColor Cyan
    docker-compose --profile cpu up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Waiting for service to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        
        # Test health endpoint
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 10
            if ($response.status -eq "healthy") {
                Write-Host "Health check passed" -ForegroundColor Green
            } else {
                Write-Host "Health check failed" -ForegroundColor Red
            }
        }
        catch {
            Write-Host "Failed to connect to service: $($_.Exception.Message)" -ForegroundColor Red
        }
        
        # Stop the service
        docker-compose --profile cpu down
        Write-Host "CPU deployment test completed" -ForegroundColor Green
    } else {
        Write-Host "Failed to start CPU deployment" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Function to validate environment files
function Test-EnvironmentFiles {
    Write-Host "Validating environment files..." -ForegroundColor Yellow
    
    $requiredFiles = @(".env", "config/config.yaml", "config/fusion_config.yaml", "docker-compose.yml", "Dockerfile")
    $missingFiles = @()
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-Host "Missing required files:" -ForegroundColor Red
        $missingFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
        return $false
    }
    
    Write-Host "All required files are present" -ForegroundColor Green
    return $true
}

# Main execution
Write-Host "Starting Docker environment setup..." -ForegroundColor Cyan

# Step 1: Validate environment files
if (-not (Test-EnvironmentFiles)) {
    Write-Host "Environment validation failed. Please ensure all required files are present." -ForegroundColor Red
    exit 1
}

# Step 2: Check Docker installation
if (-not (Test-DockerInstalled)) {
    Write-Host "Docker is not installed. Would you like to install Docker Desktop? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "Y" -or $response -eq "y") {
        if (Install-DockerDesktop) {
            Write-Host "Please restart your computer and run this script again to complete the setup." -ForegroundColor Yellow
            exit 0
        } else {
            Write-Host "Docker installation failed. Please install Docker Desktop manually." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Docker installation skipped. Please install Docker Desktop manually." -ForegroundColor Yellow
        exit 1
    }
}

# Step 3: Check if Docker is running
if (-not (Test-DockerRunning)) {
    Write-Host "Docker Desktop is not running. Please start Docker Desktop and run this script again." -ForegroundColor Yellow
    exit 1
}

# Step 4: Build Docker images
if (-not (Build-DockerImages)) {
    Write-Host "Docker image build failed. Please check the Dockerfile and try again." -ForegroundColor Red
    exit 1
}

# Step 5: Test deployment
if (-not (Test-DockerDeployment)) {
    Write-Host "Docker deployment test failed. Please check the logs and try again." -ForegroundColor Red
    exit 1
}

Write-Host "=== Docker Environment Setup Completed Successfully ===" -ForegroundColor Green
Write-Host "You can now run the following commands:" -ForegroundColor Cyan
Write-Host "  - CPU deployment: docker-compose --profile cpu up" -ForegroundColor White
Write-Host "  - GPU deployment: docker-compose --profile gpu up" -ForegroundColor White
Write-Host "  - Development: docker-compose --profile dev up" -ForegroundColor White
