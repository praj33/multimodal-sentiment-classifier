# GitHub Profile Push Script
# Run this after creating your GitHub repository

Write-Host "🚀 GitHub Profile Push Script" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

Write-Host "`n📋 Current Status:" -ForegroundColor Yellow
Write-Host "✅ Local repository initialized" -ForegroundColor Green
Write-Host "✅ Files committed to local git" -ForegroundColor Green
Write-Host "✅ Remote origin configured" -ForegroundColor Green
Write-Host "✅ Branch renamed to 'main'" -ForegroundColor Green

Write-Host "`n🎯 Next Steps:" -ForegroundColor Magenta
Write-Host "1. Go to https://github.com/new" -ForegroundColor White
Write-Host "2. Repository name: praj33" -ForegroundColor White
Write-Host "3. Make it Public ✅" -ForegroundColor White
Write-Host "4. DON'T initialize with README ❌" -ForegroundColor White
Write-Host "5. Click 'Create repository'" -ForegroundColor White

Write-Host "`n🔄 After creating the repository, choose an option:" -ForegroundColor Cyan
Write-Host "1. Push now (if repository is created)" -ForegroundColor White
Write-Host "2. Show push commands" -ForegroundColor White
Write-Host "3. Check current status" -ForegroundColor White

$choice = Read-Host "`nEnter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
        
        try {
            git push -u origin main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "`n🎉 SUCCESS! Your profile has been pushed to GitHub!" -ForegroundColor Green
                Write-Host "🌐 View your profile at: https://github.com/praj33" -ForegroundColor Cyan
                Write-Host "📊 GitHub will process the README and show your profile!" -ForegroundColor Blue
                
                Write-Host "`n✨ What happens next:" -ForegroundColor Magenta
                Write-Host "• GitHub Actions will start generating the snake animation" -ForegroundColor White
                Write-Host "• Your profile stats will update automatically" -ForegroundColor White
                Write-Host "• The typing animation will be visible on your profile" -ForegroundColor White
                Write-Host "• Visitors can see your professional GitHub profile!" -ForegroundColor White
            } else {
                Write-Host "`n❌ Push failed! Make sure you've created the repository on GitHub." -ForegroundColor Red
                Write-Host "Repository URL: https://github.com/praj33/praj33" -ForegroundColor Yellow
            }
        }
        catch {
            Write-Host "`n❌ Error occurred: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    "2" {
        Write-Host "`n📝 Push Commands:" -ForegroundColor Yellow
        Write-Host "==================" -ForegroundColor Yellow
        Write-Host "git push -u origin main" -ForegroundColor Green
        Write-Host "`nOr if you prefer the alias:" -ForegroundColor Blue
        Write-Host "git pom" -ForegroundColor Green
    }
    "3" {
        Write-Host "`n📊 Repository Status:" -ForegroundColor Yellow
        Write-Host "=====================" -ForegroundColor Yellow
        
        Write-Host "`nBranch:" -ForegroundColor Cyan
        git branch
        
        Write-Host "`nRemote:" -ForegroundColor Cyan
        git remote -v
        
        Write-Host "`nLast Commit:" -ForegroundColor Cyan
        git log --oneline -1
        
        Write-Host "`nFiles in Repository:" -ForegroundColor Cyan
        git ls-files
    }
    default {
        Write-Host "`n❌ Invalid choice!" -ForegroundColor Red
    }
}

Write-Host "`n📚 Additional Resources:" -ForegroundColor Blue
Write-Host "========================" -ForegroundColor Blue
Write-Host "• Setup Guide: SETUP-GUIDE.md" -ForegroundColor White
Write-Host "• Git Configuration: git-setup.ps1" -ForegroundColor White
Write-Host "• SSH Setup: ssh-setup.ps1" -ForegroundColor White
Write-Host "• GitHub Profile Help: https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile" -ForegroundColor White

Write-Host "`n🎯 Pro Tips:" -ForegroundColor Green
Write-Host "============" -ForegroundColor Green
Write-Host "• Your profile README will be visible at github.com/praj33" -ForegroundColor White
Write-Host "• The snake animation updates every 24 hours" -ForegroundColor White
Write-Host "• GitHub stats update in real-time" -ForegroundColor White
Write-Host "• You can customize colors and themes anytime" -ForegroundColor White
