# 🚀 Complete GitHub Profile & Git Workflow Setup Guide

This guide will help you set up an advanced GitHub profile and optimize your git workflow for maximum productivity.

## 📋 **Table of Contents**

1. [GitHub Profile Setup](#-github-profile-setup)
2. [Advanced Git Configuration](#-advanced-git-configuration)
3. [SSH Keys Setup](#-ssh-keys-setup)
4. [Git Workflow Optimization](#-git-workflow-optimization)
5. [Troubleshooting](#-troubleshooting)

---

## 🎯 **GitHub Profile Setup**

### **Step 1: Create Profile Repository**

1. **Go to GitHub** and create a new repository
   - Repository name: `praj33` (must match your username exactly)
   - Make it **public**
   - ✅ Initialize with README
   - ❌ Don't add .gitignore or license yet

2. **Clone the repository**
   ```bash
   git clone https://github.com/praj33/praj33.git
   cd praj33
   ```

3. **Copy the profile files**
   - Copy `README.md` from this setup to your profile repository
   - Copy `.github/workflows/snake.yml` for the snake animation
   - Copy `.gitignore` for clean repository management

### **Step 2: Customize Your Profile**

#### **🔧 Essential Customizations**

1. **Update Personal Information**
   ```markdown
   # In README.md, update these sections:
   - Your real name and location
   - Current projects and focus areas
   - Skills and technologies you actually use
   - Your real social media links
   ```

2. **Social Media Links**
   ```markdown
   # Replace these with your actual profiles:
   [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR-PROFILE)
   [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/YOUR-HANDLE)
   [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:YOUR-EMAIL)
   ```

3. **Featured Projects**
   ```markdown
   # Add your actual projects:
   ### 🚀 [Your Project Name](https://github.com/praj33/your-repo)
   > **Brief description of what your project does**
   - 🛠️ **Tech Stack:** List technologies used
   - ✨ **Key Features:** Main features and capabilities
   - 🎯 **Impact:** Results, metrics, or achievements
   ```

### **Step 3: Enable Advanced Features**

1. **GitHub Actions for Snake Animation**
   - The workflow will automatically run every 24 hours
   - It generates a snake eating your contribution graph
   - Make sure Actions are enabled in repository settings

2. **GitHub Stats Integration**
   - Stats will automatically show your GitHub activity
   - Customize themes by changing `theme=tokyonight` to other themes
   - Available themes: `dark`, `radical`, `merko`, `gruvbox`, `tokyonight`, etc.

---

## ⚙️ **Advanced Git Configuration**

### **Step 1: Run the Git Setup Script**

```powershell
# Navigate to the setup directory
cd path/to/praj33-profile

# Run the git configuration script
.\git-setup.ps1
```

### **Step 2: Manual Configuration (Alternative)**

If you prefer manual setup, here are the essential commands:

#### **Basic Configuration**
```bash
git config --global user.name "Pranav"
git config --global user.email "your-email@example.com"
git config --global core.editor "code --wait"
```

#### **Essential Aliases**
```bash
# Status and logging
git config --global alias.st "status -sb"
git config --global alias.lg "log --oneline --decorate --graph --all"

# Branch management
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.cb "checkout -b"

# Commit shortcuts
git config --global alias.cm "commit -m"
git config --global alias.ca "commit -am"
git config --global alias.amend "commit --amend"

# Push/Pull shortcuts
git config --global alias.pom "push origin main"
git config --global alias.pum "pull origin main"
```

#### **Advanced Workflow Settings**
```bash
git config --global push.default simple
git config --global pull.rebase true
git config --global rebase.autoStash true
git config --global core.autocrlf true  # For Windows
```

---

## 🔐 **SSH Keys Setup**

### **Step 1: Run SSH Setup Script**

```powershell
# Run the SSH setup script
.\ssh-setup.ps1

# Choose option 5 for complete setup
```

### **Step 2: Manual SSH Setup (Alternative)**

#### **Generate SSH Key**
```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Or RSA key (if Ed25519 not supported)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

#### **Add to SSH Agent**
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add your SSH key
ssh-add ~/.ssh/id_ed25519
```

#### **Add to GitHub**
1. Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Go to GitHub → Settings → SSH and GPG keys
3. Click "New SSH key"
4. Paste your public key and save

#### **Test Connection**
```bash
ssh -T git@github.com
```

---

## 🚀 **Git Workflow Optimization**

### **Daily Workflow Commands**

#### **Starting Work**
```bash
git st                    # Check status
git pum                   # Pull latest changes
git cb feature/new-work   # Create new branch
```

#### **During Development**
```bash
git st                    # Check what's changed
git add .                 # Stage changes
git cm "feat: add new feature"  # Commit with message
```

#### **Finishing Work**
```bash
git pom                   # Push to origin
# Create pull request on GitHub
git co main               # Switch back to main
git pum                   # Pull latest changes
git bd feature/new-work   # Delete feature branch
```

### **Advanced Workflow Tips**

#### **Commit Message Conventions**
```bash
git cm "feat: add new feature"      # New feature
git cm "fix: resolve bug in login"  # Bug fix
git cm "docs: update README"        # Documentation
git cm "style: format code"         # Code formatting
git cm "refactor: improve function" # Code refactoring
git cm "test: add unit tests"       # Adding tests
```

#### **Branch Management**
```bash
git branches              # List all branches
git cleanup              # Delete merged branches
git prune-all            # Clean up remote references
```

#### **Stash Management**
```bash
git ss "work in progress" # Stash changes
git sl                    # List stashes
git sa                    # Apply latest stash
git sp                    # Pop latest stash
```

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **SSH Connection Problems**
```bash
# Test SSH connection
ssh -T git@github.com

# If it fails, check SSH agent
ssh-add -l

# Re-add key if needed
ssh-add ~/.ssh/id_ed25519
```

#### **Git Configuration Issues**
```bash
# Check current configuration
git config --global --list

# Reset specific setting
git config --global --unset user.name
git config --global user.name "Correct Name"
```

#### **Line Ending Issues (Windows)**
```bash
# Fix line ending configuration
git config --global core.autocrlf true
git config --global core.safecrlf false
```

#### **GitHub Actions Not Working**
1. Check if Actions are enabled in repository settings
2. Verify the workflow file is in `.github/workflows/`
3. Check the Actions tab for error messages
4. Ensure repository is public (required for free Actions)

### **Performance Optimization**

#### **Large Repository Handling**
```bash
# Enable file system cache
git config --global core.fscache true
git config --global core.preloadindex true

# Optimize garbage collection
git config --global gc.auto 256
```

#### **Credential Management**
```bash
# Use credential manager (Windows)
git config --global credential.helper manager-core

# Cache credentials (Linux/Mac)
git config --global credential.helper cache
```

---

## 🎉 **Final Steps**

1. **Test Everything**
   - Verify git aliases work: `git st`, `git lg`, etc.
   - Test SSH connection: `ssh -T git@github.com`
   - Check GitHub profile displays correctly

2. **Customize Further**
   - Add more aliases based on your workflow
   - Customize VS Code git integration
   - Set up additional tools (GitKraken, SourceTree, etc.)

3. **Keep Updated**
   - Regularly update your profile README
   - Add new projects and skills
   - Keep git configuration optimized

**🚀 You're now ready for an optimized git workflow and an impressive GitHub profile!**
