"""
Main Module
Entry point for the AI Code Reviewer
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from .config_loader import ConfigLoader
from .llm_client import LLMClient
from .github_integration import GitHubIntegration
from .code_analyzer import CodeAnalyzer


def main():
    """Main entry point"""
    print("=" * 60)
    print("🤖 AI Code Reviewer Starting...")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Get PR information from environment
    pr_number = os.getenv('PR_NUMBER')
    repo_path = os.getenv('REPO_PATH', '.')
    
    if not pr_number:
        print("❌ Error: PR_NUMBER environment variable not set")
        sys.exit(1)
    
    try:
        pr_number = int(pr_number)
    except ValueError:
        print(f"❌ Error: Invalid PR_NUMBER: {pr_number}")
        sys.exit(1)
    
    try:
        # Initialize components
        print("\n📋 Loading configuration...")
        config = ConfigLoader(repo_path)
        
        print("\n🤖 Initializing LLM client...")
        llm_config = config.get_llm_config()
        
        # Get provider and model from env vars (ignore empty strings from unset GitHub secrets)
        provider = os.getenv('LLM_PROVIDER', '').strip() or llm_config['provider']
        model = os.getenv('LLM_MODEL', '').strip() or llm_config['model']
        
        llm_client = LLMClient(
            provider=provider,
            model=model,
            temperature=llm_config['temperature'],
            max_tokens=llm_config['max_tokens']
        )
        
        print("\n🔗 Connecting to GitHub...")
        github = GitHubIntegration()
        
        print("\n📥 Fetching PR information...")
        pr = github.get_pull_request(pr_number)
        files = github.get_pr_files(pr)
        
        if not files:
            print("ℹ️  No files to review in this PR")
            github.post_review_summary(
                pr, 
                "No files to review in this PR.", 
                0, 
                {'critical': 0, 'warning': 0, 'suggestion': 0}
            )
            return
        
        # Set initial status
        github.set_pr_status(pr, 'pending', 'AI code review in progress...')
        
        # Analyze code
        print(f"\n🔍 Analyzing {len(files)} file(s)...")
        analyzer = CodeAnalyzer(config, llm_client)
        results = analyzer.analyze_files(files)
        
        # Post comments
        print(f"\n💬 Posting review comments...")
        max_comments = config.get_max_comments()
        comments_posted = 0
        
        for result in results:
            filename = result['filename']
            comments = result['analysis']['comments']
            file_data = result['file_data']
            
            for comment in comments[:max_comments - comments_posted]:
                success = github.post_review_comment(
                    pr, 
                    comment, 
                    filename, 
                    pr.head.sha
                )
                if success:
                    comments_posted += 1
            
            if comments_posted >= max_comments:
                print(f"⚠️  Reached maximum comment limit ({max_comments})")
                break
        
        # Aggregate results and post summary
        print("\n📊 Generating summary...")
        aggregated = analyzer.aggregate_results(results)
        
        github.post_review_summary(
            pr,
            aggregated['summary'],
            aggregated['total_comments'],
            aggregated['severity_counts']
        )
        
        # Determine if PR should be blocked
        block_threshold = config.get_block_threshold()
        should_block = github.should_block_pr(aggregated['severity_counts'], block_threshold)
        
        if should_block:
            github.set_pr_status(
                pr, 
                'failure', 
                f"Code review found blocking issues (threshold: {block_threshold})"
            )
            print("\n🚫 PR blocked due to critical issues")
        else:
            github.set_pr_status(
                pr, 
                'success', 
                f"Code review completed - {aggregated['total_comments']} issue(s) found"
            )
            print("\n✅ PR approved")
        
        print("\n" + "=" * 60)
        print("✅ AI Code Review Complete!")
        print("=" * 60)
        print(f"Files analyzed: {aggregated['total_files']}")
        print(f"Issues found: {aggregated['total_comments']}")
        print(f"  🔴 Critical: {aggregated['severity_counts']['critical']}")
        print(f"  🟠 Warning: {aggregated['severity_counts']['warning']}")
        print(f"  🟢 Suggestion: {aggregated['severity_counts']['suggestion']}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
