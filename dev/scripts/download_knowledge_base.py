# download_knowledge_base.py - Download all learning materials to your PC

import os
import shutil
from datetime import datetime

def create_knowledge_archive():
    """Create a complete knowledge archive on your PC"""
    
    # Create archive directory
    archive_name = f"Developer_Knowledge_Archive_{datetime.now().strftime('%Y%m%d')}"
    archive_path = os.path.join(os.path.expanduser("~"), "Desktop", archive_name)
    
    print(f"🎯 Creating knowledge archive at: {archive_path}")
    os.makedirs(archive_path, exist_ok=True)
    
    # Files to copy
    knowledge_files = [
        "ESSENTIAL_DEVELOPER_KNOWLEDGE_GUIDE.md",
        "DEVELOPER_QUICK_REFERENCE.md", 
        "COMPLETE_LEARNING_ARCHIVE.md",
        "DAY_1_FINAL_VERIFICATION.md",
        "DAY_5_COMPLETION_SUMMARY.md",
        "FINAL_PROJECT_STATUS.md",
        "README.md",
        "DEPLOYMENT_SCALING_STRATEGY.md",
        "FEEDBACK_IMPLEMENTATION_SUMMARY.md"
    ]
    
    # Copy files
    copied_files = []
    for file in knowledge_files:
        if os.path.exists(file):
            shutil.copy2(file, archive_path)
            copied_files.append(file)
            print(f"✅ Copied: {file}")
        else:
            print(f"❌ Not found: {file}")
    
    # Create project structure copy
    project_structure = os.path.join(archive_path, "project_structure")
    os.makedirs(project_structure, exist_ok=True)
    
    # Copy important project files
    project_files = [
        "Dockerfile",
        "docker-compose.yml",
        ".env",
        "config/config.yaml",
        "requirements.txt",
        "api.py",
        "input_validation.py"
    ]
    
    for file in project_files:
        if os.path.exists(file):
            dest_dir = os.path.join(project_structure, os.path.dirname(file))
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(file, os.path.join(project_structure, file))
            print(f"✅ Copied project file: {file}")
    
    # Create summary file
    summary_content = f"""# 🎯 DEVELOPER KNOWLEDGE ARCHIVE

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Location**: {archive_path}

## 📚 CONTENTS:

### Learning Materials:
{chr(10).join(f"- {file}" for file in copied_files)}

### Project Structure:
- Complete project files for reference
- Docker configuration
- API implementation examples
- Configuration management examples

## 🚀 HOW TO USE:

1. **Read the guides** in order of importance:
   - ESSENTIAL_DEVELOPER_KNOWLEDGE_GUIDE.md (comprehensive)
   - DEVELOPER_QUICK_REFERENCE.md (daily use)
   - COMPLETE_LEARNING_ARCHIVE.md (session summary)

2. **Reference project files** when implementing:
   - Dockerfile (containerization)
   - docker-compose.yml (orchestration)
   - config.yaml (configuration management)
   - api.py (professional API structure)

3. **Follow the learning plan** outlined in the guides

## 🎯 NEXT STEPS:

1. Set up a daily learning schedule (30-60 minutes)
2. Apply one concept per week to real projects
3. Join developer communities for support
4. Start building your professional portfolio

**🎉 Your journey to professional software engineering starts here!**
"""
    
    with open(os.path.join(archive_path, "README.md"), "w") as f:
        f.write(summary_content)
    
    print(f"\n🎉 Knowledge archive created successfully!")
    print(f"📁 Location: {archive_path}")
    print(f"📚 Files copied: {len(copied_files)}")
    print(f"\n🎯 Open the README.md file in the archive for instructions!")
    
    return archive_path

if __name__ == "__main__":
    create_knowledge_archive()
