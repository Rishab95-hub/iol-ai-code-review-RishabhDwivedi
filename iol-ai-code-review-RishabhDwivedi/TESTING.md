# End-to-End Testing Guide

## How to Test the AI Code Reviewer

This guide walks you through testing the entire system end-to-end.

## Prerequisites

- Python 3.11+
- Git
- GitHub account
- OpenAI or Anthropic API key

## Step 1: Install Dependencies

```bash
cd ai-code-reviewer
pip install -r requirements.txt
```

## Step 2: Run the Test Script

```bash
python tests/test_script.py
```

This will check:
- ✅ Python version
- ✅ All dependencies installed
- ✅ Environment variables configured
- ✅ Project structure
- ✅ Configuration loader
- ✅ LLM connectivity
- ✅ GitHub API access
- ✅ Simulated code review

## Step 3: Local Testing (Without GitHub)

To test the code analysis locally:

```bash
# Set required environment variables
export OPENAI_API_KEY="your-key-here"

# Create a test Python file with issues
cat > test_code.py << 'EOF'
def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username='{username}'"
    return query
EOF

# Run analysis on the file
python -c "
from src.llm_client import LLMClient
from src.config_loader import ConfigLoader

config = ConfigLoader()
llm_client = LLMClient(provider='openai', model='gpt-3.5-turbo')

with open('test_code.py', 'r') as f:
    code = f.read()

result = llm_client.analyze_code(
    code_diff=code,
    file_path='test_code.py',
    focus_areas=['security', 'code_quality'],
    enabled_checks=['sql_injection']
)

print('Issues found:', len(result['comments']))
for comment in result['comments']:
    print(f'  - Line {comment.get(\"line\", \"?\")} [{comment[\"severity\"]}]: {comment[\"message\"]}')
"
```

## Step 4: GitHub Integration Test

### 4.1 Fork or Create a Test Repository

```bash
# Create a new repository on GitHub
gh repo create ai-review-test --public

# Or fork this repository
gh repo fork yourusername/ai-code-reviewer
```

### 4.2 Set Up Secrets

```bash
# Using GitHub CLI
gh secret set OPENAI_API_KEY -b"your-key-here"

# Or manually:
# Go to: Settings → Secrets and variables → Actions
# Add: OPENAI_API_KEY
```

### 4.3 Enable Workflow Permissions

1. Go to: Settings → Actions → General
2. Under "Workflow permissions":
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"
3. Click Save

### 4.4 Push the Code

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 4.5 Create a Test PR

```bash
# Create a new branch
git checkout -b test-ai-review

# Copy sample buggy files to root
cp sample-pr/buggy_user_service.py .
cp sample-pr/buggy_api_handler.py .

# Commit and push
git add buggy_*.py
git commit -m "Add code with intentional issues for AI review"
git push origin test-ai-review

# Create PR
gh pr create --title "Test AI Code Review" --body "Testing the AI reviewer with intentionally buggy code"
```

### 4.6 Watch the Review in Action

1. Go to your PR on GitHub
2. Navigate to the "Actions" tab to see the workflow running
3. Once complete, check the PR for:
   - Inline comments on specific lines
   - Summary comment with statistics
   - Status check (✅ or ❌)

## Step 5: Verify Results

Expected results on the test PR:

### Critical Issues (🔴)
- Hardcoded AWS credentials in `buggy_api_handler.py`
- SQL injection vulnerabilities in `buggy_user_service.py`
- Command injection via `os.system()` and `eval()`

### Warnings (🟠)
- MD5 password hashing (weak)
- N+1 query pattern
- Missing error handling
- Disabled SSL verification

### Suggestions (🟢)
- Missing docstrings
- Inefficient algorithms (O(n²))
- Global mutable state
- Unused methods

## Step 6: Test Configuration Changes

### 6.1 Customize Configuration

Create or edit `.ai-review.yaml`:

```yaml
focus_areas:
  security: true
  performance: false  # Disable performance checks
  
block_pr_on: "warning"  # Block on warnings, not just critical

max_comments: 10  # Limit to 10 comments

llm:
  model: "gpt-3.5-turbo"  # Use cheaper model
  temperature: 0.2
```

### 6.2 Test Configuration

```bash
git add .ai-review.yaml
git commit -m "Customize AI review configuration"
git push origin test-ai-review
```

The AI reviewer should now:
- Skip performance-related comments
- Block the PR even on warnings
- Post maximum 10 comments

## Step 7: Docker Testing

### 7.1 Build Docker Image

```bash
docker build -t ai-code-reviewer .
```

### 7.2 Run in Docker

```bash
docker run \
  -e GITHUB_TOKEN="$GITHUB_TOKEN" \
  -e GITHUB_REPOSITORY="owner/repo" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e PR_NUMBER=1 \
  ai-code-reviewer
```

## Troubleshooting

### Test Script Fails

#### "Package not installed"
```bash
pip install -r requirements.txt
```

#### "Environment variable not set"
```bash
# Create .env file
cp .env.example .env
# Edit and fill in your credentials
```

### GitHub Actions Workflow Fails

#### Check Workflow Logs
```bash
gh run list
gh run view <run-id>
```

#### Common Issues

1. **API key not found**
   - Verify secret name matches exactly: `OPENAI_API_KEY`
   - Check secret is set for the repository (not organization)

2. **Permission denied**
   - Enable workflow write permissions in Settings → Actions → General

3. **PR comments not posted**
   - Check GitHub token permissions
   - Verify workflow has `pull-requests: write` permission

4. **Rate limit exceeded**
   - Wait a few minutes
   - Use GPT-3.5-turbo instead of GPT-4
   - Reduce `max_comments` in config

### LLM API Errors

#### OpenAI
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### Rate Limits
- Free tier: 3 requests/min, 200 requests/day
- Paid tier: Higher limits
- Solution: Add delays or use cheaper models

## Performance Benchmarks

Typical processing times:

| PR Size | Files | Lines Changed | Model | Time | Cost |
|---------|-------|---------------|-------|------|------|
| Small | 1-3 | <100 | GPT-3.5 | ~30s | $0.01 |
| Small | 1-3 | <100 | GPT-4 | ~45s | $0.05 |
| Medium | 4-10 | 100-500 | GPT-3.5 | ~2m | $0.05 |
| Medium | 4-10 | 100-500 | GPT-4 | ~3m | $0.20 |
| Large | 10+ | 500+ | GPT-3.5 | ~5m | $0.15 |

## Success Criteria

✅ Test script passes all checks  
✅ Workflow runs without errors  
✅ Comments appear on PR  
✅ Summary comment is posted  
✅ Status check shows in PR  
✅ Critical issues are flagged  
✅ Configuration changes work  

## Next Steps

1. **Fine-tune Configuration**
   - Adjust severity thresholds
   - Add custom guidelines
   - Configure ignore patterns

2. **Integrate with CI/CD**
   - Add to existing pipelines
   - Set up notifications
   - Configure auto-merge rules

3. **Monitor Usage**
   - Track API costs
   - Review comment quality
   - Adjust based on feedback

## Support

- **Issues**: Open a GitHub issue
- **Questions**: Check README.md and QUICKSTART.md
- **Community**: GitHub Discussions

Happy testing! 🚀
