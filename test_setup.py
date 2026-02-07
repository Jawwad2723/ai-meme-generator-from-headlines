#!/usr/bin/env python3
"""
Test Script - Verify Installation and Configuration
"""

import sys
import os

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def check_python_version():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python version: {version.major}.{version.minor}.{version.micro} (3.10+ required)")
        return False

def check_packages():
    required = ['fastapi', 'uvicorn', 'requests', 'beautifulsoup4', 'openai', 'pydantic', 'dotenv']
    
    missing = []
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'beautifulsoup4':
                __import__('bs4')
            else:
                __import__(package)
            print_success(f"Package installed: {package}")
        except ImportError:
            print_error(f"Package missing: {package}")
            missing.append(package)
    
    return len(missing) == 0

def check_env_file():
    if os.path.exists('.env'):
        print_success(".env file found")
        return True
    else:
        print_error(".env file not found")
        print_info("Run: cp .env.example .env")
        return False

def check_env_variables():
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key',
        'IMGFLIP_USERNAME': 'Imgflip Username',
        'IMGFLIP_PASSWORD': 'Imgflip Password'
    }
    
    all_set = True
    for var, name in required_vars.items():
        value = os.getenv(var)
        if value and value != f"your-{var.lower().replace('_', '-')}-here" and len(value) > 3:
            print_success(f"{name} is set")
        else:
            print_error(f"{name} is not set or invalid")
            all_set = False
    
    return all_set

def test_imports():
    try:
        from app.config import settings
        print_success("app.config imported")
        
        from app.news_scraper import NewsScraperService
        print_success("app.news_scraper imported")
        
        from app.text_generator import MemeTextGenerator
        print_success("app.text_generator imported")
        
        from app.meme_creator import MemeCreatorService
        print_success("app.meme_creator imported")
        
        from app.main import app
        print_success("app.main imported")
        
        return True
    except Exception as e:
        print_error(f"Import failed: {str(e)}")
        return False

def main():
    print("\n" + "="*50)
    print("AI Meme Generator - Installation Check")
    print("="*50 + "\n")
    
    checks = []
    
    print(f"\n{BLUE}[1/6] Checking Python Version...{RESET}")
    checks.append(check_python_version())
    
    print(f"\n{BLUE}[2/6] Checking Required Packages...{RESET}")
    checks.append(check_packages())
    
    print(f"\n{BLUE}[3/6] Checking .env File...{RESET}")
    env_exists = check_env_file()
    checks.append(env_exists)
    
    if env_exists:
        print(f"\n{BLUE}[4/6] Checking Environment Variables...{RESET}")
        checks.append(check_env_variables())
    else:
        print(f"\n{BLUE}[4/6] Skipping Environment Variable Check{RESET}")
        checks.append(False)
    
    print(f"\n{BLUE}[5/6] Testing Module Imports...{RESET}")
    checks.append(test_imports())
    
    print(f"\n{BLUE}[6/6] Overall Status{RESET}")
    if all(checks):
        print_success("All checks passed! ✨")
        print_info("\nYou can now start the server:")
        print_info("  ./run.sh")
        print_info("  OR")
        print_info("  uvicorn app.main:app --reload")
        return 0
    else:
        print_error("Some checks failed. Please fix the issues above.")
        print_info("\nCommon fixes:")
        print_info("  1. Install packages: pip install -r requirements.txt")
        print_info("  2. Create .env file: cp .env.example .env")
        print_info("  3. Add your API keys to .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())