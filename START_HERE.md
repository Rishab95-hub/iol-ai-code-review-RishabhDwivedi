# 🚀 GET STARTED IN 3 STEPS

## Step 1: Install & Configure (2 minutes)

### Windows:
```cmd
cd ai-code-reviewer
pip install -r requirements.txt
copy .env.example .env
notepad .env
```

### Linux/Mac:
```bash
cd ai-code-reviewer
pip install -r requirements.txt
cp .env.example .env
nano .env
```

### Edit .env and add your API key:
```bash
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Step 2: Test Locally (1 minute)

### Option A: Quick Demo (No GitHub needed)
```bash
python demo.py
```

### Option B: Full Test Suite
```bash
# Windows
run_tests.bat

# Linux/Mac
chmod +x run_tests.sh
./run_tests.sh
```

## Step 3: Deploy to GitHub (3 minutes)

### 1. Create/Use a GitHub Repository
```bash
# If you haven't already, initialize git
git init
git add .
git commit -m "Initial commit: AI Code Reviewer"

# Create repo on GitHub (using gh cli)
gh repo create ai-code-reviewer --public --source=. --remote=origin --push

# Or push to existing repo
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### 2. Add GitHub Secret
```bash
# Using GitHub CLI
gh secret set OPENAI_API_KEY

# Or manually:
# 1. Go to: https://github.com/yourusername/your-repo/settings/secrets/actions
# 2. Click "New repository secret"
# 3. Name: OPENAI_API_KEY
# 4. Value: your-api-key
# 5. Click "Add secret"
```

### 3. Enable Workflow Permissions
1. Go to: Settings → Actions → General
2. Under "Workflow permissions":
   - ✅ Select "Read and write permissions"
   - ✅ Check "Allow GitHub Actions to create and approve pull requests"
3. Click "Save"

### 4. Test with Sample PR
```bash
# Create test branch
git checkout -b test-ai-review

# Add buggy files
git add sample-pr/buggy_user_service.py sample-pr/buggy_api_handler.py
git commit -m "Add test files with intentional bugs"
git push origin test-ai-review

# Create PR (using gh cli)
gh pr create --title "Test AI Review" --body "Testing AI code reviewer"

# Or manually: Go to GitHub and create PR from test-ai-review to main
```

## ✅ Success! 

Watch your PR for:
- ⏳ GitHub Actions workflow running
- 💬 AI posting comments on issues it finds
- 📊 Summary comment with statistics
- ✅/❌ Status check based on severity

---

## 📚 What to Read Next

- **QUICKSTART.md** - Detailed 5-minute setup guide
- **TESTING.md** - Comprehensive testing instructions
- **README.md** - Complete documentation
- **PROJECT_SUMMARY.md** - Technical overview

## 🆘 Common Issues

### "No LLM API key found"
→ Make sure you set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env

### "GITHUB_TOKEN not set" (local testing)
→ This is only needed for GitHub integration, not for demo.py

### "Permission denied" on GitHub Actions
→ Enable write permissions in Settings → Actions → General

### "Rate limit exceeded"
→ Wait a few minutes or use GPT-3.5-turbo instead of GPT-4

## 💡 Pro Tips

1. **Start with demo.py** - Test locally before deploying
2. **Use GPT-3.5-turbo** - Faster and cheaper for testing
3. **Check sample-pr/** - See example buggy code
4. **Customize .ai-review.yaml** - Tune to your needs
5. **Run tests/** - Validate everything works

---

**Need Help?** Open an issue on GitHub!

**Ready for Production?** See README.md for advanced configuration.
