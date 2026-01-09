"""
End-to-End Testing Script for AI Code Reviewer
This script validates the setup and tests the code review functionality
"""
import os
import sys
from pathlib import Path
import subprocess
import json

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(message):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")


def check_python_version():
    """Check if Python version is 3.11+"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version >= (3, 11):
        print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print_error(f"Python 3.11+ required, but {version.major}.{version.minor} found")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print_info("Checking dependencies...")
    
    required_packages = [
        'openai',
        'anthropic',
        'github',
        'yaml',
        'requests',
        'dotenv',
        'jsonschema',
        'git'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'yaml':
                __import__('yaml')
            elif package == 'github':
                __import__('github')
            elif package == 'dotenv':
                __import__('dotenv')
            elif package == 'git':
                __import__('git')
            else:
                __import__(package)
            print_success(f"Package '{package}' is installed")
        except ImportError:
            print_error(f"Package '{package}' is NOT installed")
            all_installed = False
    
    if not all_installed:
        print_warning("Install missing packages with: pip install -r requirements.txt")
    
    return all_installed


def check_environment_variables():
    """Check if required environment variables are set"""
    print_info("Checking environment variables...")
    
    # Load .env file if exists
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        print_info(f"Loaded environment from {env_file}")
    else:
        print_warning("No .env file found. Using system environment variables.")
    
    required_vars = ['GITHUB_TOKEN']
    optional_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'AZURE_OPENAI_API_KEY']
    
    all_present = True
    
    # Check required variables
    for var in required_vars:
        if os.getenv(var):
            print_success(f"{var} is set")
        else:
            print_error(f"{var} is NOT set (required)")
            all_present = False
    
    # Check at least one LLM API key is present
    llm_keys_present = any(os.getenv(var) for var in optional_vars)
    
    if llm_keys_present:
        for var in optional_vars:
            if os.getenv(var):
                print_success(f"{var} is set")
    else:
        print_error("No LLM API key found. Set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, or AZURE_OPENAI_API_KEY")
        all_present = False
    
    return all_present


def check_project_structure():
    """Verify project structure is correct"""
    print_info("Checking project structure...")
    
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        'src/main.py',
        'src/config_loader.py',
        'src/llm_client.py',
        'src/github_integration.py',
        'src/code_analyzer.py',
        '.github/workflows/ai-review.yml',
        'requirements.txt',
        'Dockerfile',
        '.ai-review.yaml',
        'README.md'
    ]
    
    all_present = True
    
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print_success(f"{file_path} exists")
        else:
            print_error(f"{file_path} is missing")
            all_present = False
    
    return all_present


def test_config_loader():
    """Test configuration loader"""
    print_info("Testing configuration loader...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src.config_loader import ConfigLoader
        
        # Test with default config
        config = ConfigLoader()
        
        # Verify config methods work
        focus_areas = config.get_focus_areas()
        llm_config = config.get_llm_config()
        max_comments = config.get_max_comments()
        
        print_success(f"Config loaded successfully")
        print_info(f"  Focus areas: {', '.join(focus_areas)}")
        print_info(f"  LLM provider: {llm_config['provider']}")
        print_info(f"  Max comments: {max_comments}")
        
        return True
    except Exception as e:
        print_error(f"Config loader test failed: {str(e)}")
        return False


def test_llm_connectivity():
    """Test LLM API connectivity"""
    print_info("Testing LLM connectivity...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src.llm_client import LLMClient
        
        # Determine which provider to test
        if os.getenv('OPENAI_API_KEY'):
            provider = 'openai'
            model = os.getenv('LLM_MODEL', 'gpt-4o-mini')  # Use cost-effective model for testing
        elif os.getenv('ANTHROPIC_API_KEY'):
            provider = 'anthropic'
            model = 'claude-3-haiku-20240307'
        elif os.getenv('AZURE_OPENAI_API_KEY'):
            provider = 'azure_openai'
            model = 'gpt-35-turbo'
        else:
            print_error("No LLM API key configured")
            return False
        
        print_info(f"Testing {provider} with model {model}...")
        
        # Initialize client
        client = LLMClient(provider=provider, model=model, max_tokens=500)
        
        # Test with simple code
        test_code = """
def hello():
    password = "admin123"  # Hardcoded password
    return password
"""
        
        result = client.analyze_code(
            code_diff=test_code,
            file_path="test.py",
            focus_areas=["security"],
            enabled_checks=["hardcoded_secrets"]
        )
        
        if result and 'comments' in result:
            print_success(f"LLM connectivity test passed")
            print_info(f"  Found {len(result['comments'])} issue(s) in test code")
            return True
        else:
            print_error("LLM returned unexpected response")
            return False
            
    except Exception as e:
        print_error(f"LLM connectivity test failed: {str(e)}")
        print_warning("Note: This is expected if API keys are not configured")
        return False


def test_github_integration():
    """Test GitHub API connectivity"""
    print_info("Testing GitHub integration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('GITHUB_TOKEN'):
        print_warning("GITHUB_TOKEN not set, skipping GitHub test")
        return True
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from github import Github, Auth
        
        auth = Auth.Token(os.getenv('GITHUB_TOKEN'))
        github = Github(auth=auth)
        user = github.get_user()
        
        print_success(f"Connected to GitHub as: {user.login}")
        rate_limit = github.get_rate_limit()
        print_info(f"  API rate limit: {rate_limit.rate.remaining}/{rate_limit.rate.limit}")
        
        return True
    except Exception as e:
        print_error(f"GitHub integration test failed: {str(e)}")
        return False


def simulate_code_review():
    """Simulate a code review on sample files"""
    print_info("Simulating code review on sample files...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src.config_loader import ConfigLoader
        from src.llm_client import LLMClient
        from src.code_analyzer import CodeAnalyzer
        
        # Load sample file
        sample_file = Path(__file__).parent.parent / 'sample-pr' / 'buggy_user_service.py'
        
        if not sample_file.exists():
            print_warning("Sample file not found, skipping simulation")
            return True
        
        with open(sample_file, 'r') as f:
            code = f.read()
        
        # Create minimal diff format
        diff = "\n".join([f"+ {line}" for line in code.split('\n')])
        
        # Initialize components
        config = ConfigLoader()
        llm_config = config.get_llm_config()
        
        # Determine provider
        if os.getenv('OPENAI_API_KEY'):
            provider = 'openai'
            model = os.getenv('LLM_MODEL', 'gpt-4o-mini')
        elif os.getenv('ANTHROPIC_API_KEY'):
            provider = 'anthropic'
            model = 'claude-3-haiku-20240307'
        else:
            print_warning("No LLM API key configured, skipping simulation")
            return True
        
        llm_client = LLMClient(provider=provider, model=model, max_tokens=500)
        analyzer = CodeAnalyzer(config, llm_client)
        
        # Analyze
        files = [{
            'filename': 'buggy_user_service.py',
            'patch': diff[:2000],  # Limit for testing
            'status': 'modified'
        }]
        
        results = analyzer.analyze_files(files)
        
        if results:
            print_success("Code review simulation completed")
            for result in results:
                print_info(f"  File: {result['filename']}")
                print_info(f"  Issues found: {len(result['analysis']['comments'])}")
        else:
            print_warning("No issues found in simulation")
        
        return True
        
    except Exception as e:
        print_error(f"Simulation failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print_header("🧪 AI Code Reviewer - End-to-End Testing")
    
    tests = [
        ("Python Version Check", check_python_version),
        ("Dependencies Check", check_dependencies),
        ("Environment Variables Check", check_environment_variables),
        ("Project Structure Check", check_project_structure),
        ("Configuration Loader Test", test_config_loader),
        ("LLM Connectivity Test", test_llm_connectivity),
        ("GitHub Integration Test", test_github_integration),
        ("Code Review Simulation", simulate_code_review),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print_header(test_name)
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_error(f"Test crashed: {str(e)}")
            results[test_name] = False
    
    # Print summary
    print_header("📊 Test Summary")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print_success("\n🎉 All tests passed! The AI Code Reviewer is ready to use.")
        return 0
    else:
        print_warning(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
