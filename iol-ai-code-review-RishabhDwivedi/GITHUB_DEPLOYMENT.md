# 🚀 Complete GitHub Deployment Guide

## Current Status
✅ Code is ready
✅ Git is initialized  
✅ API keys are configured

## ⚠️ IMPORTANT: Before You Start

**Make sure your .env file is NOT committed!**

Check that `.env` is in `.gitignore`:
```powershell
Get-Content .gitignore | Select-String ".env"
```

Should show: `.env` ✅

If you accidentally committed .env, remove it:
```powershell
git rm --cached .env
git commit -m "Remove .env from git"
```

## Step-by-Step Deployment

### Step 0: Commit Any Pending Changes (1 min)

```powershell
cd "c:\Users\risdwivedi\Desktop\Personal\Code assistance\ai-code-reviewer"

# Check what needs to be committed
git status

# Add all new/modified files (except .env which is in .gitignore)
git add .

# Commit changes
git commit -m "Update AI Code Reviewer with fixes and improvements"
```

### Step 1: Create GitHub Repository (2 min)

1. Go to: **https://github.com/new**
2. Fill in:
   - Repository name: `ai-code-reviewer`
   - Description: "AI-powered code review assistant"
   - Visibility: **Public** ✅
   - **DO NOT check** "Initialize with README"
3. Click "Create repository"

### Step 2: Push Code to GitHub (1 min)

After creating the repo, run these commands:

```powershell
cd "c:\Users\risdwivedi\Desktop\Personal\Code assistance\ai-code-reviewer"

# Add remote (replace YOUR-USERNAME with Rishab95-hub)
git remote add origin https://github.com/Rishab95-hub/ai-code-reviewer.git

# Rename branch to main
git branch -M main

# Push code
git push -u origin main
```

### Step 3: Add OpenAI API Key as Secret (1 min)

1. Go to: **https://github.com/Rishab95-hub/ai-code-reviewer/settings/secrets/actions**
2. Click **"New repository secret"**
3. Add secret:
   - Name: `OPENAI_API_KEY`
   - Value: (Get from your .env file - the value after `OPENAI_API_KEY=`)
4. Click **"Add secret"**

**To get your key from .env:**
```powershell
# View your API key (for copying)
Get-Content .env | Select-String "OPENAI_API_KEY"
```

Copy only the key value (after the `=`), not the `OPENAI_API_KEY=` part!

### Step 4: Enable Workflow Permissions (30 sec)

1. Go to: **https://github.com/Rishab95-hub/ai-code-reviewer/settings/actions**
2. Scroll to "Workflow permissions"
3. Select: **"Read and write permissions"** ✅
4. Check: **"Allow GitHub Actions to create and approve pull requests"** ✅
5. Click **"Save"**

### Step 5: Create Test Branch with Buggy Code (2 min)

```powershell
cd "c:\Users\risdwivedi\Desktop\Personal\Code assistance\ai-code-reviewer"

# Create new branch
git checkout -b test-ai-review

# Copy buggy files to root
Copy-Item sample-pr\buggy_user_service.py .
Copy-Item sample-pr\buggy_api_handler.py .

# Commit changes
git add buggy_user_service.py buggy_api_handler.py
git commit -m "Add test files with intentional bugs"

# Push branch
git push origin test-ai-review
```

### Step 6: Create Pull Request (1 min)

1. Go to: **https://github.com/Rishab95-hub/ai-code-reviewer**
2. You'll see a banner: "test-ai-review had recent pushes"
3. Click **"Compare & pull request"**
4. Title: "Test AI Code Review"
5. Description: "Testing the AI reviewer with intentionally buggy code"
6. Click **"Create pull request"**

### Step 7: Watch the Magic! ✨

1. Go to the **"Actions"** tab to see workflow running
2. Wait 1-2 minutes for analysis
3. Return to your PR to see:
   - ✅ Inline comments on specific lines
   - ✅ Summary comment with statistics
   - ✅ Status check (pass/fail)

## Expected Results

The AI should find approximately:

### 🔴 Critical Issues (5-8)
- Hardcoded AWS credentials
- SQL injection vulnerabilities
- Command injection (eval, os.system)
- Weak MD5 hashing
- Insecure deserialization

### 🟠 Warnings (5-10)
- N+1 query patterns
- Missing error handling
- Disabled SSL verification
- Path traversal risks
- Logging sensitive data

### 🟢 Suggestions (3-5)
- Missing docstrings
- No type hints
- Inefficient algorithms
- Code smells

## Troubleshooting

### If workflow doesn't run:
- Check that `.github/workflows/ai-review.yml` exists in repository
- Verify workflow permissions are enabled
- Check Actions tab for error messages
- Make sure you created a PR (not just pushed to a branch)

### If no comments appear:
- Check workflow logs in Actions tab (click on the workflow run)
- Verify OPENAI_API_KEY secret is set correctly (no spaces, quotes, or extra characters)
- Ensure workflow has write permissions
- Check that files aren't in `ignore_patterns` in `.ai-review.yaml`

### If you get "401 Unauthorized" errors:
- Your OpenAI API key is invalid or expired
- Get a new key from https://platform.openai.com/api-keys
- Update the GitHub secret with the new key

### If workflow fails with "No PR_NUMBER":
- Make sure you're creating a Pull Request, not just pushing
- The workflow only runs on PR events (opened, synchronize, reopened)

### If costs are too high:
- The default model is already `gpt-4o-mini` (very cheap)
- You can further reduce costs by editing `.ai-review.yaml`:
  - Set `max_comments: 10` (reduce number of comments)
  - Add more patterns to `ignore_patterns`
  - Disable some focus areas

### Check workflow is working:
```powershell
# After creating PR, check if Actions are running
# Go to: https://github.com/Rishab95-hub/ai-code-reviewer/actions
```

## Quick Commands Reference

```powershell
# View current branch
git branch

# Check remote
git remote -v

# View commit history
git log --oneline

# Check workflow status (if you install gh cli)
gh run list

# View specific workflow run
gh run view <run-id>
```

## Cost Estimate

This test PR will cost approximately:
- **$0.05 - $0.15** (with gpt-4o-mini)
- Processing time: 1-2 minutes

## Next Steps After Successful PR

1. ✅ Review the AI comments
2. ✅ Verify accuracy of issues found
3. ✅ Customize `.ai-review.yaml` for your needs
4. ✅ Use in real projects!

---

## ✅ Pre-Flight Checklist

Before starting deployment, verify:

- [ ] `.env` file exists locally with valid `OPENAI_API_KEY`
- [ ] `.env` is in `.gitignore` (check with: `Get-Content .gitignore | Select-String ".env"`)
- [ ] You tested locally with `python demo.py` and it worked
- [ ] All files are committed (`git status` shows clean working tree or pending changes)
- [ ] GitHub token has correct permissions (Contents: Read, PRs: Read/Write, Workflows: Read/Write)

## 🎯 Quick Start Commands

If you're ready to go, run these in order:

```powershell
# 1. Navigate to project
cd "c:\Users\risdwivedi\Desktop\Personal\Code assistance\ai-code-reviewer"

# 2. Make sure .env is NOT being tracked
git status | Select-String ".env"
# Should show nothing (if .env appears, run: git rm --cached .env)

# 3. Commit any changes
git add .
git commit -m "Prepare AI Code Reviewer for deployment"

# 4. Add remote (AFTER creating repo on GitHub)
git remote add origin https://github.com/Rishab95-hub/ai-code-reviewer.git

# 5. Push to GitHub
git branch -M main
git push -u origin main

# 6. Create test branch
git checkout -b test-ai-review
Copy-Item sample-pr\buggy_user_service.py .
Copy-Item sample-pr\buggy_api_handler.py .
git add buggy_*.py
git commit -m "Add test files with intentional bugs"
git push origin test-ai-review
```

Then go to GitHub to:
- Add OPENAI_API_KEY secret
- Enable workflow permissions
- Create the PR

---

**Ready?** Start with the Pre-Flight Checklist above! 🚀
