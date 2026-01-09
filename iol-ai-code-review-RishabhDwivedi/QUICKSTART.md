# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add:
# - GITHUB_TOKEN (from https://github.com/settings/tokens)
# - OPENAI_API_KEY (from https://platform.openai.com/api-keys)
```

### 3. Add GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions:

- Add secret: `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`)

### 4. Enable Workflow

Push the workflow file to your repository:
```bash
git add .github/workflows/ai-review.yml
git commit -m "Add AI code review workflow"
git push
```

### 5. Test It!

```bash
# Create test branch
git checkout -b test-review

# Add sample buggy code
git add sample-pr/
git commit -m "Test AI review"
git push origin test-review

# Create PR on GitHub and watch the magic! ✨
```

## Troubleshooting

### "GITHUB_TOKEN not set"
- Make sure you've added the secret in repository settings
- Check workflow permissions are set to "Read and write"

### "No LLM API key found"
- Verify you've added OPENAI_API_KEY or ANTHROPIC_API_KEY as a secret
- Check the secret name matches exactly

### "Permission denied"
- Go to Settings → Actions → General
- Enable "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### Rate Limits
- OpenAI: 3 requests/min (free tier)
- GitHub: 5000 requests/hour
- Consider using GPT-3.5-turbo for higher throughput

## Next Steps

- Customize `.ai-review.yaml` for your project
- Adjust severity thresholds
- Add custom guidelines
- Integrate with CI/CD pipeline

Need help? Open an issue!
