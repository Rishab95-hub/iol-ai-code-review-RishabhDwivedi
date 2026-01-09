# 🔄 AI Code Review Workflow Diagram

## High-Level Flow

```
Developer Creates PR
         |
         v
GitHub Actions Triggered
         |
         v
AI Code Reviewer Starts
         |
         v
┌────────┴─────────┐
│   Load Config    │
│ (.ai-review.yaml)│
└────────┬─────────┘
         |
         v
┌────────┴─────────┐
│  Initialize LLM  │
│ (OpenAI/etc)     │
└────────┬─────────┘
         |
         v
┌────────┴─────────┐
│  Fetch PR Files  │
│  & Diffs         │
└────────┬─────────┘
         |
         v
┌────────┴─────────┐
│  For Each File   │
│  Do Analysis     │
└────────┬─────────┘
         |
         v
┌────────┴─────────┐
│ Send to LLM for  │
│ Review           │
└────────┬─────────┘
         |
         v
┌────────┴─────────┐
│ Parse Results    │
│ & Comments       │
└────────┬─────────┘
         |
         v
┌────────┴─────────┐
│ Post Comments    │
│ on PR            │
└────────┬─────────┘
         |
         v
┌────────┴─────────┐
│ Set PR Status    │
│ (✅ or ❌)       │
└────────┬─────────┘
         |
         v
Developer Reviews Feedback
```

## Detailed Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                        GITHUB                               │
│  ┌──────────┐                                               │
│  │   Pull   │  Webhook                                      │
│  │  Request │  ──────────────┐                              │
│  └──────────┘                │                              │
└────────────────────────────────┼──────────────────────────┘
                                 │
                                 v
┌─────────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS                            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Workflow: .github/workflows/ai-review.yml           │  │
│  │                                                       │  │
│  │  1. Checkout code                                    │  │
│  │  2. Setup Python                                     │  │
│  │  3. Install dependencies                             │  │
│  │  4. Run: python -m src.main                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           v
┌─────────────────────────────────────────────────────────────┐
│                     MAIN ORCHESTRATOR                       │
│                      (src/main.py)                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Load environment variables                       │   │
│  │ 2. Get PR number from env                           │   │
│  └─────────────────────────────────────────────────────┘   │
│           │            │            │            │          │
└───────────┼────────────┼────────────┼────────────┼──────────┘
            │            │            │            │
            v            v            v            v
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Config     │ │     LLM      │ │   GitHub     │ │    Code      │
│   Loader     │ │   Client     │ │ Integration  │ │  Analyzer    │
├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤
│              │ │              │ │              │ │              │
│• Load YAML   │ │• Initialize  │ │• Connect to  │ │• Parse diffs │
│• Validate    │ │  provider    │ │  GitHub API  │ │• Filter      │
│• Get rules   │ │• Build       │ │• Fetch files │ │  files       │
│• Apply       │ │  prompts     │ │• Get diffs   │ │• Chunk large │
│  filters     │ │• Call API    │ │• Post        │ │  files       │
│              │ │• Parse       │ │  comments    │ │• Aggregate   │
│              │ │  response    │ │• Set status  │ │  results     │
│              │ │              │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
       │                 │                 │                 │
       └─────────────────┴─────────────────┴─────────────────┘
                                │
                                v
                    ┌───────────────────────┐
                    │   Analysis Results    │
                    │                       │
                    │ • Comments with       │
                    │   - Line numbers      │
                    │   - Severity          │
                    │   - Category          │
                    │   - Suggestions       │
                    │ • Summary stats       │
                    └───────────────────────┘
                                │
                                v
                      Back to GitHub PR
                    (Comments + Status)
```

## Analysis Flow Detail

```
Input: Changed Files
         │
         ├─→ File 1: app.py
         │   │
         │   ├─→ Check ignore patterns? → Skip if matches
         │   │
         │   ├─→ Extract diff/patch
         │   │
         │   ├─→ Chunk if too large (>12KB)
         │   │
         │   ├─→ Build analysis prompt:
         │   │   • File path
         │   │   • Code diff
         │   │   • Focus areas (security, performance, etc)
         │   │   • Enabled checks
         │   │   • Custom guidelines
         │   │
         │   ├─→ Send to LLM API
         │   │
         │   ├─→ Receive JSON response:
         │   │   {
         │   │     "comments": [
         │   │       {
         │   │         "line": 42,
         │   │         "severity": "critical",
         │   │         "category": "security",
         │   │         "message": "SQL injection vulnerability",
         │   │         "suggestion": "Use parameterized queries"
         │   │       }
         │   │     ],
         │   │     "summary": "Found security issues..."
         │   │   }
         │   │
         │   ├─→ Parse & validate response
         │   │
         │   └─→ Store results
         │
         ├─→ File 2: utils.py
         │   └─→ (same process)
         │
         └─→ File 3: config.js
             └─→ (same process)
         
Aggregate All Results
         │
         ├─→ Deduplicate comments
         ├─→ Sort by severity
         ├─→ Count by type
         └─→ Generate summary
         
Post to GitHub
         │
         ├─→ For each comment:
         │   ├─→ Try inline comment (line-specific)
         │   └─→ Fallback to general comment if fails
         │
         ├─→ Post summary comment with stats
         │
         └─→ Set PR status:
             ├─→ ✅ Success (if no blocking issues)
             └─→ ❌ Failure (if critical issues found)
```

## Configuration Impact

```
.ai-review.yaml
      │
      ├─→ ignore_patterns
      │   └─→ Filter out files before analysis
      │
      ├─→ focus_areas
      │   └─→ Tell LLM what to focus on
      │
      ├─→ block_pr_on
      │   └─→ Determine if PR should be blocked
      │
      ├─→ max_comments
      │   └─→ Limit number of comments posted
      │
      ├─→ llm.provider
      │   └─→ Choose OpenAI/Anthropic/Azure
      │
      ├─→ llm.model
      │   └─→ Choose specific model
      │
      └─→ checks
          └─→ Enable/disable specific checks
```

## Error Handling Flow

```
Every Step
    │
    ├─→ Try operation
    │
    ├─→ Catch errors
    │
    └─→ Handle gracefully:
        ├─→ Log error message
        ├─→ Continue with next file/step
        ├─→ Post general comment if critical
        └─→ Set appropriate PR status
```

## Rate Limiting Strategy

```
Before API Call
      │
      ├─→ Check rate limit status
      │
      ├─→ If near limit:
      │   └─→ Wait/delay
      │
      └─→ Make call with retry logic:
          ├─→ Try call
          ├─→ If rate limited: wait & retry
          └─→ If persistent failure: skip & log
```

## Comment Posting Strategy

```
For Each Issue Found
      │
      ├─→ Has line number?
      │   │
      │   ├─→ YES: Try inline comment
      │   │   ├─→ Success? → Done
      │   │   └─→ Failed? → Post as general
      │   │
      │   └─→ NO: Post as general comment
      │
      └─→ Format with:
          ├─→ Severity emoji (🔴/🟠/🟢)
          ├─→ Category
          ├─→ Message
          └─→ Suggestion (if available)
```

## Severity Decision Tree

```
Issue Found
    │
    ├─→ Is it a security vulnerability?
    │   └─→ YES: 🔴 CRITICAL
    │
    ├─→ Does it cause bugs/crashes?
    │   └─→ YES: 🔴 CRITICAL
    │
    ├─→ Performance impact?
    │   └─→ YES: 🟠 WARNING
    │
    ├─→ Code quality issue?
    │   └─→ YES: 🟠 WARNING
    │
    └─→ Style/docs improvement?
        └─→ YES: 🟢 SUGGESTION
```

---

## Key Takeaways

1. **Automated**: Triggers on every PR
2. **Configurable**: Controlled by .ai-review.yaml
3. **Multi-provider**: Works with different LLMs
4. **Graceful**: Handles errors without breaking
5. **Informative**: Posts detailed, actionable comments
6. **Status aware**: Sets PR pass/fail based on severity

---

This workflow ensures comprehensive, automated code review with minimal manual intervention!
