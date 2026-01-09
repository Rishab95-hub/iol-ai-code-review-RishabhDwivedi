#!/usr/bin/env python3
"""
Simple Setup Wizard for AI Code Reviewer
Helps users get started quickly
"""
import os
import sys
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required (you have {sys.version_info.major}.{sys.version_info.minor})")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True
    except:
        print("❌ Failed to install dependencies")
        return False


def setup_env_file():
    """Set up .env file"""
    print("\nSetting up environment file...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("Overwrite? (y/n): ").lower()
        if response != 'y':
            print("Keeping existing .env")
            return True
    
    if env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env from template")
    else:
        # Create minimal .env
        with open(env_file, 'w') as f:
            f.write("# GitHub Configuration\n")
            f.write("GITHUB_TOKEN=\n\n")
            f.write("# LLM API Keys (set at least one)\n")
            f.write("OPENAI_API_KEY=\n")
            f.write("ANTHROPIC_API_KEY=\n")
        print("✅ Created new .env file")
    
    return True


def configure_api_keys():
    """Help user configure API keys"""
    print("\nConfiguring API keys...")
    print("\nYou need at least one LLM API key:")
    print("1. OpenAI: https://platform.openai.com/api-keys")
    print("2. Anthropic: https://console.anthropic.com/")
    print("3. Azure OpenAI: https://portal.azure.com/")
    
    env_file = Path(".env")
    
    print("\nWhich provider do you want to use?")
    print("1. OpenAI (recommended for beginners)")
    print("2. Anthropic")
    print("3. Azure OpenAI")
    print("4. Skip (I'll configure manually)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "4":
        print("\n⚠️  Remember to edit .env file manually!")
        return True
    
    if choice == "1":
        print("\nOpenAI API Key setup:")
        print("1. Visit: https://platform.openai.com/api-keys")
        print("2. Create a new API key")
        print("3. Copy the key (starts with 'sk-')")
        api_key = input("\nPaste your OpenAI API key: ").strip()
        
        if api_key:
            with open(env_file, 'r') as f:
                content = f.read()
            content = content.replace('OPENAI_API_KEY=', f'OPENAI_API_KEY={api_key}')
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ OpenAI API key configured")
            return True
    
    elif choice == "2":
        print("\nAnthropic API Key setup:")
        print("1. Visit: https://console.anthropic.com/")
        print("2. Create a new API key")
        print("3. Copy the key (starts with 'sk-ant-')")
        api_key = input("\nPaste your Anthropic API key: ").strip()
        
        if api_key:
            with open(env_file, 'r') as f:
                content = f.read()
            content = content.replace('ANTHROPIC_API_KEY=', f'ANTHROPIC_API_KEY={api_key}')
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ Anthropic API key configured")
            return True
    
    print("⚠️  API key not configured. Please edit .env manually.")
    return False


def run_demo():
    """Offer to run demo"""
    print("\n" + "=" * 70)
    print("Setup complete! 🎉")
    print("=" * 70)
    
    print("\nWhat would you like to do next?")
    print("1. Run quick demo (analyze sample code)")
    print("2. Run full test suite")
    print("3. Open documentation")
    print("4. Exit and configure manually")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Running demo...\n")
        import subprocess
        subprocess.call([sys.executable, "demo.py"])
    
    elif choice == "2":
        print("\n🧪 Running tests...\n")
        import subprocess
        subprocess.call([sys.executable, "tests/test_script.py"])
    
    elif choice == "3":
        print("\n📚 Documentation files:")
        print("  - START_HERE.md - Quick 3-step guide")
        print("  - QUICKSTART.md - 5-minute setup")
        print("  - README.md - Complete documentation")
        print("  - TESTING.md - Testing guide")
    
    print("\n✅ All done! Check START_HERE.md for next steps.")


def main():
    """Main setup wizard"""
    print_header("🤖 AI Code Reviewer - Setup Wizard")
    
    print("This wizard will help you set up the AI Code Reviewer.\n")
    
    steps = [
        ("Check Python version", check_python_version),
        ("Install dependencies", install_dependencies),
        ("Set up environment file", setup_env_file),
        ("Configure API keys", configure_api_keys),
    ]
    
    for step_name, step_func in steps:
        print_header(step_name)
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the issue and run setup again.")
            return 1
    
    run_demo()
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
