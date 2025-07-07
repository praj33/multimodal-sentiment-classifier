# Advanced Git Configuration Setup Script
# Run this script to configure your git environment for optimal workflow

Write-Host "🚀 Setting up Advanced Git Configuration..." -ForegroundColor Cyan

# Basic Configuration
Write-Host "📝 Setting up basic git configuration..." -ForegroundColor Yellow
git config --global user.name "Pranav"
git config --global user.email "praj33@example.com"  # Update with your real email

# Editor Configuration
Write-Host "🔧 Setting up editor configuration..." -ForegroundColor Yellow
git config --global core.editor "code --wait"  # Use VS Code as default editor
git config --global merge.tool "vscode"
git config --global mergetool.vscode.cmd "code --wait $MERGED"
git config --global diff.tool "vscode"
git config --global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"

# Line Ending Configuration (Important for Windows)
Write-Host "📄 Setting up line ending configuration..." -ForegroundColor Yellow
git config --global core.autocrlf true
git config --global core.safecrlf false

# Performance and Security
Write-Host "⚡ Setting up performance and security..." -ForegroundColor Yellow
git config --global core.preloadindex true
git config --global core.fscache true
git config --global gc.auto 256
git config --global credential.helper manager-core

# Advanced Aliases
Write-Host "🎯 Setting up advanced git aliases..." -ForegroundColor Yellow

# Status and Log Aliases
git config --global alias.st "status -sb"
git config --global alias.ss "status"
git config --global alias.lg "log --oneline --decorate --graph --all"
git config --global alias.lol "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.hist "log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short"

# Branch Management
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.cb "checkout -b"
git config --global alias.bd "branch -d"
git config --global alias.bD "branch -D"
git config --global alias.branches "branch -a"
git config --global alias.remotes "remote -v"

# Commit Aliases
git config --global alias.ci "commit"
git config --global alias.cm "commit -m"
git config --global alias.ca "commit -am"
git config --global alias.amend "commit --amend"
git config --global alias.amendne "commit --amend --no-edit"

# Stash Aliases
git config --global alias.sl "stash list"
git config --global alias.sa "stash apply"
git config --global alias.ss "stash save"
git config --global alias.sp "stash pop"
git config --global alias.sd "stash drop"

# Diff and Merge Aliases
git config --global alias.df "diff"
git config --global alias.dc "diff --cached"
git config --global alias.dt "difftool"
git config --global alias.mt "mergetool"

# Remote Aliases
git config --global alias.pu "push"
git config --global alias.pl "pull"
git config --global alias.pom "push origin main"
git config --global alias.pum "pull origin main"
git config --global alias.fo "fetch origin"
git config --global alias.fu "fetch upstream"

# Advanced Workflow Aliases
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
git config --global alias.visual "!gitk"
git config --global alias.type "cat-file -t"
git config --global alias.dump "cat-file -p"
git config --global alias.find "!git ls-files | grep -i"

# Cleanup Aliases
git config --global alias.cleanup "!git branch --merged | grep -v '\*\|main\|master\|develop' | xargs -n 1 git branch -d"
git config --global alias.prune-all "!git remote | xargs -n 1 git remote prune"

# Advanced Features
Write-Host "🔥 Setting up advanced features..." -ForegroundColor Yellow
git config --global push.default simple
git config --global pull.rebase true
git config --global rebase.autoStash true
git config --global branch.autosetupmerge always
git config --global branch.autosetuprebase always

# Color Configuration
Write-Host "🎨 Setting up color configuration..." -ForegroundColor Yellow
git config --global color.ui auto
git config --global color.branch.current "yellow reverse"
git config --global color.branch.local yellow
git config --global color.branch.remote green
git config --global color.diff.meta "yellow bold"
git config --global color.diff.frag "magenta bold"
git config --global color.diff.old "red bold"
git config --global color.diff.new "green bold"
git config --global color.status.added yellow
git config --global color.status.changed green
git config --global color.status.untracked cyan

# GPG Signing (Optional - uncomment if you want to sign commits)
# Write-Host "🔐 Setting up GPG signing..." -ForegroundColor Yellow
# git config --global commit.gpgsign true
# git config --global user.signingkey YOUR_GPG_KEY_ID

Write-Host "✅ Git configuration completed successfully!" -ForegroundColor Green
Write-Host "🎉 You can now use advanced git aliases and features!" -ForegroundColor Cyan

# Display current configuration
Write-Host "`n📋 Current Git Configuration:" -ForegroundColor Magenta
git config --global --list | Sort-Object
