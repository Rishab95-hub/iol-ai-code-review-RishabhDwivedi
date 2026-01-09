# 🎯 HOW TO TEST THIS PROJECT - STEP BY STEP

## ⚡ FASTEST PATH TO TESTING (5 MINUTES)

### Step 1: Navigate to the Project (30 seconds)
```powershell
cd "c:\Users\risdwivedi\Desktop\Personal\Code assistance\ai-code-reviewer"
```

### Step 2: Install Dependencies (1 minute)
```powershell
pip install -r requirements.txt
```

### Step 3: Set Up API Key (2 minutes)
```powershell
# Copy the example environment file
copy .env.example .env

# Edit .env and add your API key
notepad .env
```

In the `.env` file, add your API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```
Save and close.

### Step 4: Run the Demo (1 minute)
```powershell
python demo.py
```

**Expected Output:**
- ✅ Code analysis runs
- ✅ Multiple issues detected (security, performance, etc.)
- ✅ Detailed feedback with line numbers
- ✅ Severity levels shown (🔴/🟠/🟢)

### Step 5: Run Full Tests (1 minute)
```powershell
python tests\test_script.py
```

**Expected Output:**
- ✅ 8 tests run
- ✅ All tests pass (or show what needs configuration)

---

## 🔄 ALTERNATIVE: INTERACTIVE SETUP

```powershell
python setup_wizard.py
```

This will:
1. Check Python version
2. Install dependencies
3. Create .env file
4. Help you configure API keys
5. Run the demo automatically

---

## 🌐 DEPLOY TO GITHUB (10 MINUTES)

### Prerequisites
- GitHub account
- Git installed
- GitHub CLI (optional but recommended)

### Step 1: Initialize Git Repository
```powershell
cd "c:\Users\risdwivedi\Desktop\Personal\Code assistance\ai-code-reviewer"
git init
git add .
git commit -m "Initial commit: AI Code Reviewer"
```

### Step 2: Create GitHub Repository

**Option A: Using GitHub CLI (Easiest)**
```powershell
gh repo create ai-code-reviewer --public --source=. --remote=origin --push
```

**Option B: Manual**
1. Go to https://github.com/new
2. Create repository named "ai-code-reviewer"
3. Don't initialize with README (we already have one)
4. Run:
```powershell
git remote add origin https://github.com/YOUR-USERNAME/ai-code-reviewer.git
git branch -M main
git push -u origin main
```

### Step 3: Add GitHub Secret

**Option A: Using GitHub CLI**
```powershell
gh secret set OPENAI_API_KEY
# Paste your API key when prompted
```

**Option B: Manual**
1. Go to your repository on GitHub
2. Click Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `OPENAI_API_KEY`
5. Value: Your API key
6. Click "Add secret"

### Step 4: Enable Workflow Permissions
1. Go to Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click "Save"

### Step 5: Create Test PR
```powershell
# Create a new branch
git checkout -b test-ai-review

# Add the buggy sample files to root for testing
copy sample-pr\buggy_user_service.py .
copy sample-pr\buggy_api_handler.py .

# Commit and push
git add buggy_user_service.py buggy_api_handler.py
git commit -m "Add test files with intentional bugs"
git push origin test-ai-review
```

### Step 6: Create Pull Request

**Option A: Using GitHub CLI**
```powershell
gh pr create --title "Test AI Code Review" --body "Testing the AI reviewer with intentionally buggy code"
```

**Option B: Manual**
1. Go to your repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Select "test-ai-review" branch
4. Click "Create pull request"

### Step 7: Watch the Magic! ✨

1. Go to your PR on GitHub
2. Click the "Actions" tab to watch workflow run
3. Wait 1-2 minutes for analysis
4. Check your PR for:
   - Inline comments on specific issues
   - Summary comment with statistics
   - Status check (✅ or ❌)

**Expected Results:**
- 15-25 comments posted
- Issues categorized by severity
- Security vulnerabilities flagged as 🔴 CRITICAL
- Performance issues as 🟠 WARNING
- Style suggestions as 🟢 SUGGESTION

---

## 📊 WHAT ISSUES SHOULD BE DETECTED

In the sample files, the AI should find:

### 🔴 CRITICAL Issues
- Hardcoded AWS credentials
- SQL injection vulnerabilities
- Command injection (eval, os.system)
- Insecure deserialization (pickle)

### 🟠 WARNING Issues
- MD5 password hashing (weak)
- N+1 query patterns
- Missing error handling
- Disabled SSL verification
- Path traversal vulnerability

### 🟢 SUGGESTIONS
- Missing docstrings
- Inefficient algorithms (O(n²))
- Global mutable state
- Unused methods
- Missing type hints

---

## 🔍 VERIFICATION CHECKLIST

After deployment, verify:

- [ ] GitHub Actions workflow appears in repository
- [ ] Workflow runs when PR is created
- [ ] Workflow completes successfully
- [ ] Comments appear on PR
- [ ] Comments are on correct lines
- [ ] Summary comment shows statistics
- [ ] Status check appears (green or red)
- [ ] Critical issues are flagged correctly

---

## 🐛 TROUBLESHOOTING

### "No module named 'openai'"
**Solution:** Run `pip install -r requirements.txt`

### "OPENAI_API_KEY not found"
**Solution:** Make sure you created `.env` file and added your API key

### "GitHub Actions workflow not running"
**Solution:**
1. Check workflow file exists: `.github/workflows/ai-review.yml`
2. Check workflow permissions in Settings → Actions → General
3. Make sure secret is named exactly: `OPENAI_API_KEY`

### "Rate limit exceeded"
**Solution:**
- Wait a few minutes
- Or use GPT-3.5-turbo instead of GPT-4
- Edit `.ai-review.yaml` and change model

### "No comments posted on PR"
**Solution:**
1. Check Actions tab for error logs
2. Verify OPENAI_API_KEY secret is set correctly
3. Check workflow permissions (need write access)
4. Look for error messages in workflow logs

---

## 💰 COST ESTIMATES

### Local Testing (demo.py)
- One run: ~$0.01 - $0.02 (with GPT-3.5-turbo)
- Essentially free for testing

### GitHub PR Review
- Small PR (<100 lines): $0.01 - $0.05
- Medium PR (100-500 lines): $0.05 - $0.10
- Large PR (>500 lines): $0.10 - $0.30

**Optimization Tips:**
- Use GPT-3.5-turbo instead of GPT-4 (10x cheaper)
- Set `max_comments: 20` in `.ai-review.yaml`
- Add files to `ignore_patterns` that don't need review

---

## 📚 DOCUMENTATION REFERENCE

Quick guides:
- **START_HERE.md** - 3-step quick start
- **QUICKSTART.md** - 5-minute setup
- **FINAL_README.md** - What was created

Detailed docs:
- **README.md** - Complete documentation
- **TESTING.md** - All testing scenarios
- **WORKFLOW_DIAGRAM.md** - Visual flow diagrams

Reference:
- **PROJECT_SUMMARY.md** - Technical overview
- **VALIDATION_CHECKLIST.md** - Quality validation
- **config-schema.json** - Configuration options

---

## ✅ SUCCESS CRITERIA

You'll know it's working when:

1. **Local Test Passes**
   - `python demo.py` runs successfully
   - Issues are detected in sample code
   - Output shows severity levels

2. **GitHub Integration Works**
   - Workflow runs automatically on PR
   - Comments appear on PR
   - Summary is posted
   - Status check shows

3. **Quality of Reviews**
   - Critical issues are flagged as 🔴
   - Comments are on correct lines
   - Suggestions are actionable
   - No false positives (or very few)

---

## 🎓 LEARNING PROGRESSION

### Level 1: Just Make It Work
1. Run `python demo.py`
2. See it detect issues
3. Understand the output

### Level 2: Deploy to GitHub
1. Follow GitHub deployment steps
2. Create test PR
3. Watch it review automatically

### Level 3: Customize
1. Edit `.ai-review.yaml`
2. Add your own rules
3. Tune severity thresholds
4. Optimize for your workflow

### Level 4: Advanced
1. Study the code in `src/`
2. Add new checks
3. Integrate with other tools
4. Contribute improvements

---

## 🚀 START NOW!

The fastest way to see it in action:

```powershell
cd "c:\Users\risdwivedi\Desktop\Personal\Code assistance\ai-code-reviewer"
python setup_wizard.py
```

Then follow the prompts!

---

## 📞 NEED HELP?

1. **Check documentation** - START_HERE.md, QUICKSTART.md, README.md
2. **Review sample code** - See what issues should be detected
3. **Run tests** - `python tests\test_script.py` shows what's missing
4. **Check logs** - GitHub Actions shows detailed error messages

---

**Ready to begin? Start with:** `python setup_wizard.py`

🎉 **Good luck!**
