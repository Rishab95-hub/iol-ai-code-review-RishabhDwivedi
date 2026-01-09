"""
Quick Demo Script - Test AI Code Review Locally
This script demonstrates the code analysis without needing GitHub
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm_client import LLMClient
from src.config_loader import ConfigLoader
from dotenv import load_dotenv
import os


def print_banner():
    print("=" * 70)
    print("  🤖 AI Code Reviewer - Quick Demo")
    print("=" * 70)
    print()


def demo_code_analysis():
    """Demonstrate code analysis on sample buggy code"""
    
    print_banner()
    
    # Load environment
    load_dotenv()
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY') and not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Error: No LLM API key found!")
        print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file")
        return
    
    # Sample buggy code
    buggy_code = '''
def authenticate_user(username, password):
    """Authenticate user - CONTAINS INTENTIONAL BUGS"""
    # ISSUE: Hardcoded credentials
    admin_password = "admin123"
    
    # ISSUE: SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    # ISSUE: No error handling
    result = database.execute(query)
    
    # ISSUE: Weak password hashing
    import hashlib
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    return result

def process_payment(card_number, amount):
    # ISSUE: Logging sensitive data
    print(f"Processing payment: {card_number} for ${amount}")
    
    # ISSUE: No validation
    total = amount
    return total
'''
    
    print("📝 Sample Code to Analyze:")
    print("-" * 70)
    print(buggy_code)
    print("-" * 70)
    print()
    
    # Initialize components
    print("🔧 Initializing AI Code Reviewer...")
    
    config = ConfigLoader()
    
    # Determine provider
    if os.getenv('OPENAI_API_KEY'):
        provider = 'openai'
        model = os.getenv('LLM_MODEL', 'gpt-4o-mini')
        print(f"✅ Using OpenAI ({model})")
    elif os.getenv('ANTHROPIC_API_KEY'):
        provider = 'anthropic'
        model = 'claude-3-haiku-20240307'
        print(f"✅ Using Anthropic ({model})")
    else:
        print("❌ No API key found")
        return
    
    print()
    print("🔍 Analyzing code for issues...")
    print()
    
    # Create LLM client
    llm_client = LLMClient(
        provider=provider,
        model=model,
        temperature=0.3,
        max_tokens=1500
    )
    
    # Analyze the code
    result = llm_client.analyze_code(
        code_diff=buggy_code,
        file_path="demo.py",
        focus_areas=config.get_focus_areas(),
        enabled_checks=config.get_enabled_checks(),
        custom_guidelines=config.get_custom_guidelines()
    )
    
    # Display results
    print("=" * 70)
    print("  📊 ANALYSIS RESULTS")
    print("=" * 70)
    print()
    
    if not result.get('comments'):
        print("✨ No issues found!")
        return
    
    # Count by severity
    severity_counts = {'critical': 0, 'warning': 0, 'suggestion': 0}
    for comment in result['comments']:
        severity = comment.get('severity', 'suggestion')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    print(f"Total Issues Found: {len(result['comments'])}")
    print(f"  🔴 Critical: {severity_counts['critical']}")
    print(f"  🟠 Warning: {severity_counts['warning']}")
    print(f"  🟢 Suggestion: {severity_counts['suggestion']}")
    print()
    
    # Display each comment
    severity_emoji = {
        'critical': '🔴',
        'warning': '🟠',
        'suggestion': '🟢'
    }
    
    for i, comment in enumerate(result['comments'], 1):
        emoji = severity_emoji.get(comment.get('severity', 'suggestion'), '⚪')
        severity = comment.get('severity', 'suggestion').upper()
        category = comment.get('category', 'general').replace('_', ' ').title()
        line = comment.get('line', '?')
        message = comment.get('message', 'No message')
        suggestion = comment.get('suggestion', '')
        
        print(f"\n{i}. {emoji} {severity} - {category}")
        print(f"   Line: {line}")
        print(f"   Issue: {message}")
        
        if suggestion:
            print(f"   💡 Suggestion: {suggestion}")
    
    # Display summary
    if result.get('summary'):
        print()
        print("=" * 70)
        print("  📝 SUMMARY")
        print("=" * 70)
        print()
        print(result['summary'])
    
    print()
    print("=" * 70)
    print("  ✅ Demo Complete!")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("1. Review the issues found above")
    print("2. Run 'python tests/test_script.py' for full validation")
    print("3. Push to GitHub and create a PR to see it in action")
    print("4. Check README.md for complete documentation")
    print()


if __name__ == "__main__":
    try:
        demo_code_analysis()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease ensure:")
        print("1. You have installed dependencies: pip install -r requirements.txt")
        print("2. You have set API keys in .env file")
        print("3. You are running from the project root directory")
