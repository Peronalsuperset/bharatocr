#!/usr/bin/env python3
"""
Cloud Deployment Preparation Script
Helps prepare BharatDoc AI-OCR for cloud deployment
"""

import os
import shutil
import sys
from pathlib import Path

def create_deployment_package():
    """Create a clean deployment package."""
    print("🚀 Creating Cloud Deployment Package")
    print("=" * 50)
    
    # Create deployment directory
    deploy_dir = Path("deployment_package")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Files to include
    files_to_copy = [
        "streamlit_app_cloud.py",
        "requirements_cloud.txt",
        "Procfile",
        "runtime.txt",
        "railway.json",
        "Dockerfile",
        "docker-compose.yml",
        "DEPLOYMENT_GUIDE.md",
        "README_SIMPLE.md"
    ]
    
    # Directories to copy
    dirs_to_copy = [
        "core",
        ".streamlit"
    ]
    
    print("📁 Copying files...")
    
    # Copy individual files
    for file_name in files_to_copy:
        src = Path(file_name)
        if src.exists():
            shutil.copy2(src, deploy_dir / file_name)
            print(f"✅ Copied {file_name}")
        else:
            print(f"⚠️  File not found: {file_name}")
    
    # Copy directories
    for dir_name in dirs_to_copy:
        src = Path(dir_name)
        if src.exists():
            shutil.copytree(src, deploy_dir / dir_name)
            print(f"✅ Copied directory: {dir_name}")
        else:
            print(f"⚠️  Directory not found: {dir_name}")
    
    # Create .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
temp/
tmp/

# Logs
*.log

# Data files (if any)
data/
uploads/
"""
    
    with open(deploy_dir / ".gitignore", "w", encoding='utf-8') as f:
        f.write(gitignore_content.strip())
    
    print("✅ Created .gitignore")
    
    # Create README for deployment
    readme_content = """# BharatDoc AI-OCR - Cloud Deployment

This is a cloud-ready deployment package for BharatDoc AI-OCR.

## Quick Deploy

### Streamlit Cloud (Recommended)
1. Upload all files to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file: `streamlit_app_cloud.py`
5. Deploy!

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Railway
1. Connect to GitHub repository
2. Railway will auto-detect configuration
3. Deploy automatically

### Docker
```bash
docker build -t bharatdoc-ocr .
docker run -p 8501:8501 bharatdoc-ocr
```

## Features
- ✅ No local dependencies required
- ✅ Works on all major cloud platforms
- ✅ Automatic PDF processing
- ✅ Multi-language support
- ✅ JSON/CSV export

## Support
See DEPLOYMENT_GUIDE.md for detailed instructions.
"""
    
    with open(deploy_dir / "README.md", "w", encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README.md")
    
    print(f"\n🎉 Deployment package created at: {deploy_dir.absolute()}")
    print("\n📋 Next steps:")
    print("1. Upload the contents of 'deployment_package' to GitHub")
    print("2. Follow the deployment guide for your chosen platform")
    print("3. Share your deployed URL!")
    
    return deploy_dir

def validate_deployment_package(deploy_dir):
    """Validate the deployment package."""
    print(f"\n🔍 Validating deployment package...")
    
    required_files = [
        "streamlit_app_cloud.py",
        "requirements_cloud.txt",
        "core/processor_simple.py",
        "core/language/detect.py",
        "core/parsing/udhyam_parser.py",
        "core/output/json_output.py",
        "core/output/csv_output.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (deploy_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Main function."""
    print("🇮🇳 BharatDoc AI-OCR - Cloud Deployment Preparation")
    print("=" * 60)
    
    # Create deployment package
    deploy_dir = create_deployment_package()
    
    # Validate package
    if validate_deployment_package(deploy_dir):
        print("\n🎊 Deployment package is ready!")
        print(f"📁 Location: {deploy_dir.absolute()}")
        print("\n🚀 Ready to deploy on:")
        print("   • Streamlit Cloud (Free)")
        print("   • Heroku (Free tier)")
        print("   • Railway (Free tier)")
        print("   • Docker (Anywhere)")
        print("   • Google Cloud Run")
        print("   • AWS App Runner")
    else:
        print("\n❌ Deployment package validation failed!")
        print("Please check the missing files and try again.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 