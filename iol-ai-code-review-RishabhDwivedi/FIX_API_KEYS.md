# 🔑 How to Fix API Key Issues

## Issue You're Seeing

```
❌ Error: Incorrect API key provided
❌ GitHub integration test failed: 401 Bad credentials
```

## Quick Fix (2 minutes)

### Step 1: Get Valid OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. **Important:** Copy the key immediately (starts with `sk-proj-...`)
5. Name it something like "AI Code Reviewer"

### Step 2: Update Your .env File

```powershell
notepad .env
```

**Replace the old key with your new key:**

```bash
# Change this:
OPENAI_API_KEY=sk-proj-old-wrong-key-here

# To your actual key:
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# Optional: Specify model (now defaults to gpt-4o-mini)
LLM_MODEL=gpt-4o-mini
```

Save and close.

### Step 3: (Optional) Fix GitHub Token

If you want to test GitHub integration:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "AI Code Reviewer Test"
4. Select scopes:
   - ✅ `repo` (full control)
   - ✅ `workflow` (update workflows)
5. Click "Generate token"
6. Copy the token (starts with `ghp_...`)

**Add to .env:**
```bash
GITHUB_TOKEN=ghp_YOUR_ACTUAL_GITHUB_TOKEN
```

### Step 4: Test Again

```powershell
python demo.py
```

**OR run full tests:**

```powershell
python tests\test_script.py
```

---

## ✅ Updated Default Model

The system now uses **gpt-4o-mini** by default - it's:
- ✅ Faster than GPT-3.5-turbo
- ✅ More cost-effective
- ✅ Better quality responses
- ✅ Released in 2024

**Cost comparison per 1M tokens:**
- GPT-4o-mini: $0.15 (input) / $0.60 (output)
- GPT-3.5-turbo: $0.50 (input) / $1.50 (output)
- GPT-4: $30 (input) / $60 (output)

---

## Testing Without API Keys

You can still test the project structure without API keys:

```powershell
# Test just the structure and config
python -c "from src.config_loader import ConfigLoader; c = ConfigLoader(); print('Config loaded:', c.get_focus_areas())"

# Check dependencies
pip list | Select-String "openai|anthropic|github|PyGithub"
```

---

## Common Mistakes

### ❌ Wrong: Partial key in .env
```
OPENAI_API_KEY=sk-proj-...truncated...
```

### ✅ Correct: Full key in .env
```
OPENAI_API_KEY=sk-proj-Abc123XyZ789FullKeyHereDoNotTruncate
```

### ❌ Wrong: Quotes around key
```
OPENAI_API_KEY="sk-proj-123"
```

### ✅ Correct: No quotes
```
OPENAI_API_KEY=sk-proj-123
```

---

## Quick Test Command

Once you've updated your API key:

```powershell
# Quick test (costs ~$0.01)
python demo.py
```

**Expected output:**
```
✅ Using OpenAI (gpt-4o-mini)
🔍 Analyzing code for issues...
📊 ANALYSIS RESULTS
Total Issues Found: 5
  🔴 Critical: 2
  🟠 Warning: 2
  🟢 Suggestion: 1
```

---

## Still Having Issues?

### Check your .env file format:
```powershell
Get-Content .env
```

Should look like:
```
GITHUB_TOKEN=ghp_your_token
OPENAI_API_KEY=sk-proj-your_key
LLM_MODEL=gpt-4o-mini
```

### Verify API key works:
```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key loaded:', os.getenv('OPENAI_API_KEY')[:20] + '...' if os.getenv('OPENAI_API_KEY') else 'NOT FOUND')"
```

---

## Don't Have an OpenAI Account?

**Option 1:** Use Anthropic instead
- Go to: https://console.anthropic.com/
- Get API key
- Add to .env: `ANTHROPIC_API_KEY=sk-ant-...`
- Change config: `LLM_PROVIDER=anthropic`

**Option 2:** Skip AI testing for now
- The project structure is complete
- You can deploy to GitHub
- Add API key as GitHub Secret later

---

## Next Step

After fixing your API key:

```powershell
# Test locally
python demo.py

# If that works, run full tests
python tests\test_script.py

# Then deploy to GitHub (see QUICKSTART.md)
```

✅ **You're almost there!** Just need valid API keys.
