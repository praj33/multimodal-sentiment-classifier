# SSH Keys Setup Script for GitHub
# This script helps you generate and configure SSH keys for GitHub

Write-Host "🔐 SSH Keys Setup for GitHub" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if SSH directory exists
$sshDir = "$env:USERPROFILE\.ssh"
if (!(Test-Path $sshDir)) {
    Write-Host "📁 Creating SSH directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $sshDir -Force
}

# Function to generate SSH key
function Generate-SSHKey {
    param(
        [string]$email,
        [string]$keyName = "id_ed25519"
    )
    
    Write-Host "🔑 Generating SSH key..." -ForegroundColor Yellow
    
    # Generate SSH key using Ed25519 algorithm (recommended)
    $keyPath = "$sshDir\$keyName"
    ssh-keygen -t ed25519 -C $email -f $keyPath -N '""'
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SSH key generated successfully!" -ForegroundColor Green
        return $keyPath
    } else {
        Write-Host "❌ Failed to generate SSH key!" -ForegroundColor Red
        return $null
    }
}

# Function to start SSH agent and add key
function Add-SSHKeyToAgent {
    param([string]$keyPath)
    
    Write-Host "🚀 Starting SSH agent..." -ForegroundColor Yellow
    
    # Start SSH agent
    Start-Service ssh-agent
    
    # Add SSH key to agent
    ssh-add $keyPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SSH key added to agent!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to add SSH key to agent!" -ForegroundColor Red
    }
}

# Function to display public key
function Show-PublicKey {
    param([string]$keyPath)
    
    $publicKeyPath = "$keyPath.pub"
    if (Test-Path $publicKeyPath) {
        Write-Host "`n📋 Your public SSH key:" -ForegroundColor Magenta
        Write-Host "========================" -ForegroundColor Magenta
        Get-Content $publicKeyPath
        Write-Host "========================" -ForegroundColor Magenta
        
        # Copy to clipboard
        Get-Content $publicKeyPath | Set-Clipboard
        Write-Host "📎 Public key copied to clipboard!" -ForegroundColor Green
    }
}

# Function to test SSH connection
function Test-GitHubSSH {
    Write-Host "`n🧪 Testing SSH connection to GitHub..." -ForegroundColor Yellow
    ssh -T git@github.com
}

# Main execution
Write-Host "`nChoose an option:" -ForegroundColor Cyan
Write-Host "1. Generate new SSH key" -ForegroundColor White
Write-Host "2. Add existing SSH key to agent" -ForegroundColor White
Write-Host "3. Display existing public key" -ForegroundColor White
Write-Host "4. Test GitHub SSH connection" -ForegroundColor White
Write-Host "5. Complete setup (all steps)" -ForegroundColor White

$choice = Read-Host "`nEnter your choice (1-5)"

switch ($choice) {
    "1" {
        $email = Read-Host "Enter your GitHub email"
        $keyPath = Generate-SSHKey -email $email
        if ($keyPath) {
            Add-SSHKeyToAgent -keyPath $keyPath
            Show-PublicKey -keyPath $keyPath
        }
    }
    "2" {
        $keyName = Read-Host "Enter SSH key name (default: id_ed25519)"
        if ([string]::IsNullOrEmpty($keyName)) { $keyName = "id_ed25519" }
        $keyPath = "$sshDir\$keyName"
        Add-SSHKeyToAgent -keyPath $keyPath
    }
    "3" {
        $keyName = Read-Host "Enter SSH key name (default: id_ed25519)"
        if ([string]::IsNullOrEmpty($keyName)) { $keyName = "id_ed25519" }
        $keyPath = "$sshDir\$keyName"
        Show-PublicKey -keyPath $keyPath
    }
    "4" {
        Test-GitHubSSH
    }
    "5" {
        Write-Host "`n🚀 Complete SSH setup..." -ForegroundColor Cyan
        $email = Read-Host "Enter your GitHub email"
        
        # Generate key
        $keyPath = Generate-SSHKey -email $email
        if ($keyPath) {
            # Add to agent
            Add-SSHKeyToAgent -keyPath $keyPath
            
            # Show public key
            Show-PublicKey -keyPath $keyPath
            
            Write-Host "`n📝 Next steps:" -ForegroundColor Yellow
            Write-Host "1. Go to GitHub.com → Settings → SSH and GPG keys" -ForegroundColor White
            Write-Host "2. Click 'New SSH key'" -ForegroundColor White
            Write-Host "3. Paste the public key (already copied to clipboard)" -ForegroundColor White
            Write-Host "4. Give it a title (e.g., 'My Windows PC')" -ForegroundColor White
            Write-Host "5. Click 'Add SSH key'" -ForegroundColor White
            Write-Host "6. Run this script again and choose option 4 to test" -ForegroundColor White
        }
    }
    default {
        Write-Host "❌ Invalid choice!" -ForegroundColor Red
    }
}

Write-Host "`n📚 Additional SSH Configuration:" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Magenta

# Create SSH config file
$configPath = "$sshDir\config"
$configContent = @"
# GitHub configuration
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

# GitHub Enterprise (if you use it)
Host github-enterprise.com
    HostName github-enterprise.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

# GitLab (if you use it)
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
"@

if (!(Test-Path $configPath)) {
    Write-Host "📝 Creating SSH config file..." -ForegroundColor Yellow
    $configContent | Out-File -FilePath $configPath -Encoding UTF8
    Write-Host "✅ SSH config file created!" -ForegroundColor Green
} else {
    Write-Host "📄 SSH config file already exists at: $configPath" -ForegroundColor Blue
}

Write-Host "`n🎉 SSH setup completed!" -ForegroundColor Green
