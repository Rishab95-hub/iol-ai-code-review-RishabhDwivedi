"""
GitHub Integration Module
Handles interaction with GitHub API for PR analysis and commenting
"""
import os
from typing import List, Dict, Any, Optional
from github import Github, Auth, GithubException
from github.PullRequest import PullRequest
from github.Repository import Repository


class GitHubIntegration:
    """Handles GitHub API interactions"""
    
    SEVERITY_EMOJIS = {
        'critical': '🔴',
        'warning': '🟠',
        'suggestion': '🟢'
    }
    
    def __init__(self, token: str = None, repo_name: str = None):
        """Initialize GitHub client"""
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.repo_name = repo_name or os.getenv('GITHUB_REPOSITORY')
        
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        if not self.repo_name:
            raise ValueError("GITHUB_REPOSITORY environment variable not set")
        
        try:
            auth = Auth.Token(self.token)
            self.github = Github(auth=auth)
            self.repo = self.github.get_repo(self.repo_name)
            print(f"✅ Connected to GitHub repository: {self.repo_name}")
        except GithubException as e:
            raise Exception(f"Failed to connect to GitHub: {str(e)}")
    
    def get_pull_request(self, pr_number: int) -> PullRequest:
        """Get pull request by number"""
        try:
            pr = self.repo.get_pull(pr_number)
            print(f"✅ Retrieved PR #{pr_number}: {pr.title}")
            return pr
        except GithubException as e:
            raise Exception(f"Failed to get PR #{pr_number}: {str(e)}")
    
    def get_pr_files(self, pr: PullRequest) -> List[Dict[str, Any]]:
        """Get all files changed in the PR with their diffs"""
        files_data = []
        
        try:
            files = pr.get_files()
            for file in files:
                if file.patch:  # Only process files with actual changes
                    files_data.append({
                        'filename': file.filename,
                        'status': file.status,  # added, modified, removed
                        'additions': file.additions,
                        'deletions': file.deletions,
                        'patch': file.patch,
                        'sha': file.sha
                    })
            
            print(f"✅ Retrieved {len(files_data)} changed files from PR")
            return files_data
        except GithubException as e:
            raise Exception(f"Failed to get PR files: {str(e)}")
    
    def post_review_comment(self, pr: PullRequest, comment: Dict[str, Any], 
                           file_path: str, commit_sha: str) -> bool:
        """Post a review comment on a specific line"""
        try:
            severity_emoji = self.SEVERITY_EMOJIS.get(comment['severity'], '⚪')
            category = comment['category'].replace('_', ' ').title()
            
            # Build comment body
            body = f"{severity_emoji} **{comment['severity'].upper()}** - {category}\n\n"
            body += f"{comment['message']}\n"
            
            if comment.get('suggestion'):
                body += f"\n💡 **Suggestion:**\n{comment['suggestion']}"
            
            # Try to post inline comment if line number is available
            if comment.get('line') and isinstance(comment['line'], int):
                try:
                    pr.create_review_comment(
                        body=body,
                        commit=self.repo.get_commit(commit_sha),
                        path=file_path,
                        line=comment['line']
                    )
                    return True
                except GithubException as e:
                    # If inline comment fails, fall back to regular comment
                    print(f"⚠️ Failed to post inline comment: {e}. Posting as general comment.")
                    pr.create_issue_comment(body=f"**{file_path}**\n{body}")
                    return True
            else:
                # Post as general PR comment
                pr.create_issue_comment(body=f"**{file_path}**\n{body}")
                return True
                
        except Exception as e:
            print(f"❌ Failed to post comment: {str(e)}")
            return False
    
    def post_review_summary(self, pr: PullRequest, summary: str, 
                           total_comments: int, severity_counts: Dict[str, int]) -> bool:
        """Post a summary comment on the PR"""
        try:
            body = f"## 🤖 AI Code Review Summary\n\n"
            body += f"{summary}\n\n"
            body += f"### 📊 Statistics\n"
            body += f"- Total issues found: {total_comments}\n"
            body += f"- 🔴 Critical: {severity_counts.get('critical', 0)}\n"
            body += f"- 🟠 Warning: {severity_counts.get('warning', 0)}\n"
            body += f"- 🟢 Suggestion: {severity_counts.get('suggestion', 0)}\n"
            
            pr.create_issue_comment(body)
            print("✅ Posted review summary")
            return True
        except Exception as e:
            print(f"❌ Failed to post summary: {str(e)}")
            return False
    
    def should_block_pr(self, severity_counts: Dict[str, int], threshold: str) -> bool:
        """Determine if PR should be blocked based on severity threshold"""
        threshold_map = {
            'none': [],
            'suggestion': ['suggestion', 'warning', 'critical'],
            'warning': ['warning', 'critical'],
            'critical': ['critical']
        }
        
        blocking_severities = threshold_map.get(threshold.lower(), [])
        
        for severity in blocking_severities:
            if severity_counts.get(severity, 0) > 0:
                return True
        
        return False
    
    def set_pr_status(self, pr: PullRequest, state: str, description: str, context: str = "AI Code Review"):
        """Set PR status check"""
        try:
            commit = self.repo.get_commit(pr.head.sha)
            commit.create_status(
                state=state,  # pending, success, error, failure
                description=description,
                context=context
            )
            print(f"✅ Set PR status: {state} - {description}")
        except Exception as e:
            print(f"⚠️ Failed to set PR status: {str(e)}")
    
    def get_changed_lines_map(self, patch: str) -> Dict[int, str]:
        """Parse patch to map line numbers to their content"""
        lines_map = {}
        current_new_line = 0
        
        for line in patch.split('\n'):
            if line.startswith('@@'):
                # Parse hunk header to get starting line number
                # Format: @@ -old_start,old_count +new_start,new_count @@
                try:
                    parts = line.split('+')[1].split('@@')[0].strip()
                    current_new_line = int(parts.split(',')[0])
                except:
                    continue
            elif line.startswith('+') and not line.startswith('+++'):
                # New line added
                lines_map[current_new_line] = line[1:]
                current_new_line += 1
            elif not line.startswith('-'):
                # Context line (unchanged)
                current_new_line += 1
        
        return lines_map
