# 🤖 AI-Powered Code Review Assistant

An intelligent, automated code review system that analyzes pull requests and provides context-aware, actionable feedback on code quality, security vulnerabilities, performance issues, best practices, and documentation.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Setup Instructions](#-setup-instructions)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Sample PR Demo](#-sample-pr-demo)
- [Limitations](#-limitations)
- [Contributing](#-contributing)

## ✨ Features

### 🔍 Comprehensive Code Analysis

- **Code Quality**: Identifies code smells, anti-patterns, and maintainability issues
- **Security Scanning**: Detects SQL injection, XSS, hardcoded secrets, and insecure dependencies
- **Performance Review**: Highlights inefficient algorithms, memory leaks, and N+1 query patterns
- **Best Practices**: Suggests improvements based on language/framework conventions
- **Documentation Check**: Flags missing or inadequate comments, docstrings, and README updates

### 🎯 Context-Aware Intelligence

- Understands broader codebase context (not just diffs)
- Avoids redundant or obvious comments
- Differentiates between critical issues, warnings, and suggestions
- Provides specific, actionable feedback with suggested fixes

### 📊 Severity-Based Reporting

- 🔴 **Critical**: Security vulnerabilities and breaking issues
- 🟠 **Warning**: Code quality and performance concerns
- 🟢 **Suggestion**: Style improvements and best practices

### ⚙️ Highly Configurable

- Custom ignore patterns for files/directories
- Configurable review focus areas
- Severity thresholds for blocking PRs
- Support for multiple LLM providers (OpenAI, Anthropic, Azure OpenAI)
- Custom guidelines and rules

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitHub PR Event                          │
│                    (opened/updated/reopened)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GitHub Actions Workflow                        │
│                  (.github/workflows/ai-review.yml)               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Main Orchestrator                           │
│                        (src/main.py)                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Load Configuration (.ai-review.yaml)                 │  │
│  │  2. Initialize LLM Client                                │  │
│  │  3. Connect to GitHub API                                │  │
│  │  4. Fetch PR files and diffs                             │  │
│  │  5. Analyze code with AI                                 │  │
│  │  6. Post review comments                                 │  │
│  │  7. Set PR status (pass/fail)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────┬────────────────┬──────────────┬────────────────┘
                 │                │              │
        ┌────────▼────────┐  ┌───▼────┐  ┌─────▼──────┐
        │ Config Loader   │  │  LLM   │  │  GitHub    │
        │                 │  │ Client │  │Integration │
        │ - Load config   │  │        │  │            │
        │ - Validate      │  │ OpenAI │  │ - Fetch PR │
        │ - Apply rules   │  │Anthropic│ │ - Post    │
        │                 │  │ Azure  │  │   comments│
        └─────────────────┘  └────────┘  └────────────┘
                                   │
                          ┌────────▼─────────┐
                          │  Code Analyzer   │
                          │                  │
                          │ - Parse diffs    │
                          │ - Chunk large    │
                          │   files          │
                          │ - Aggregate      │
                          │   results        │
                          │ - Deduplicate    │
                          └──────────────────┘
```

### Component Description

1. **Main Orchestrator** (`src/main.py`): Entry point that coordinates the entire review process
2. **Config Loader** (`src/config_loader.py`): Loads and validates `.ai-review.yaml` configuration
3. **LLM Client** (`src/llm_client.py`): Interfaces with various LLM providers for code analysis
4. **GitHub Integration** (`src/github_integration.py`): Handles GitHub API interactions
5. **Code Analyzer** (`src/code_analyzer.py`): Orchestrates file analysis and result aggregation

## 🚀 Setup Instructions

### Prerequisites

- Python 3.11 or higher
- GitHub account with repository access
- API key for one of the supported LLM providers:
  - OpenAI API key
  - Anthropic API key
  - Azure OpenAI credentials

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Install Dependencies

#### Using pip (Local Development)

```bash
pip install -r requirements.txt
```

#### Using Docker

```bash
docker build -t ai-code-reviewer .
```

### 3. Configure GitHub Repository

#### Set up GitHub Secrets

Go to your repository settings → Secrets and variables → Actions, and add:

```
OPENAI_API_KEY=sk-...                    # For OpenAI
# OR
ANTHROPIC_API_KEY=sk-ant-...             # For Anthropic
# OR
AZURE_OPENAI_API_KEY=...                 # For Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://...
```

**Note**: `GITHUB_TOKEN` is automatically provided by GitHub Actions.

#### Set Workflow Permissions

Go to Settings → Actions → General → Workflow permissions:
- Enable "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### 4. Add Configuration File (Optional)

Create `.ai-review.yaml` in your repository root to customize behavior:

```yaml
# Files to ignore
ignore_patterns:
  - "*.md"
  - "node_modules/**"
  - "dist/**"

# Focus areas
focus_areas:
  code_quality: true
  security: true
  performance: true
  best_practices: true
  documentation: true

# Block PR if critical issues found
block_pr_on: "critical"  # Options: critical, warning, suggestion, none

# LLM configuration
llm:
  provider: "openai"     # Options: openai, anthropic, azure_openai
  model: "gpt-4"
  temperature: 0.3
  max_tokens: 2000

# Maximum comments per PR
max_comments: 50
```

See [.ai-review.yaml](.ai-review.yaml) for a complete example.

### 5. Enable the Workflow

The workflow is automatically enabled when you push the `.github/workflows/ai-review.yml` file to your repository.

## ⚙️ Configuration

### Configuration File Schema

See [config-schema.json](config-schema.json) for the complete JSON schema.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub authentication token | Yes (auto-provided) |
| `GITHUB_REPOSITORY` | Repository name (owner/repo) | Yes (auto-provided) |
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key | If using Anthropic |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key | If using Azure |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | If using Azure |
| `LLM_PROVIDER` | Override provider from config | No |
| `LLM_MODEL` | Override model from config | No |
| `PR_NUMBER` | Pull request number | Yes (auto-set) |

### Supported LLM Providers

| Provider | Models | Notes |
|----------|--------|-------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-3.5-turbo | Recommended for best results |
| Anthropic | claude-3-opus, claude-3-sonnet | Excellent for detailed analysis |
| Azure OpenAI | Your deployed models | Enterprise option |

## 📖 Usage

### Automatic Review

Once set up, the AI reviewer automatically analyzes every pull request:

1. Create a new branch and make changes
2. Push your branch to GitHub
3. Create a pull request
4. The AI reviewer will automatically:
   - Analyze all changed files
   - Post inline comments on specific issues
   - Add a summary comment with statistics
   - Set PR status (✅ pass or ❌ fail based on severity threshold)

### Manual Testing (Local)

```bash
# Set environment variables
export GITHUB_TOKEN=your_token
export GITHUB_REPOSITORY=owner/repo
export OPENAI_API_KEY=your_key
export PR_NUMBER=123

# Run the reviewer
python -m src.main
```

### Docker Deployment

```bash
docker run -e GITHUB_TOKEN=$GITHUB_TOKEN \
           -e GITHUB_REPOSITORY=owner/repo \
           -e OPENAI_API_KEY=$OPENAI_API_KEY \
           -e PR_NUMBER=123 \
           ai-code-reviewer
```

## 🎬 Sample PR Demo

This repository includes sample files with intentional bugs for demonstration:

### Testing the Reviewer

1. **Create a test branch**:
   ```bash
   git checkout -b test-ai-review
   ```

2. **Add the buggy files** (they're already in `sample-pr/`):
   ```bash
   git add sample-pr/buggy_user_service.py sample-pr/buggy_api_handler.py
   git commit -m "Add sample code for AI review testing"
   git push origin test-ai-review
   ```

3. **Create a PR** from `test-ai-review` to `main`

4. **Watch the AI reviewer** analyze the code and post comments

### Expected Results

The AI reviewer should identify issues including:

- 🔴 **Critical**: Hardcoded AWS credentials, SQL injection vulnerabilities
- 🟠 **Warning**: MD5 password hashing, N+1 query problems
- 🟢 **Suggestion**: Missing docstrings, inefficient algorithms

See [sample-pr/README.md](sample-pr/README.md) for a complete list of intentional issues.

## 🧪 Testing

Use the provided test script to validate the setup:

```bash
python tests/test_script.py
```

This script will:
- ✅ Verify all dependencies are installed
- ✅ Check environment variables
- ✅ Validate configuration file
- ✅ Test LLM connectivity
- ✅ Simulate a code review

## ⚠️ Limitations

### Current Limitations

1. **Token Limits**: Very large PRs may hit LLM token limits
   - Mitigation: Diff chunking is implemented (configurable)

2. **API Rate Limits**: High-frequency PRs may hit API limits
   - Mitigation: Built-in rate limiting and error handling

3. **Cost**: Each PR review consumes LLM API tokens
   - Mitigation: Configure `max_comments` and use cheaper models for non-critical repos

4. **Context Window**: Limited understanding of files not in the diff
   - Mitigation: Future versions will include full repo context

5. **Language Support**: Optimized for Python, JavaScript, TypeScript, Go, Java
   - Other languages supported but may have reduced accuracy

6. **False Positives**: AI may occasionally flag non-issues
   - Mitigation: Use severity thresholds and custom guidelines

### Known Issues

- Binary files and large files (>10MB) are skipped
- Very complex regex patterns in ignore_patterns may slow processing
- Inline comments may fail on certain diff formats (falls back to general comments)

## 🔒 Security Considerations

- Never commit API keys or tokens to the repository
- Use GitHub Secrets for all sensitive credentials
- Review the code before deploying to production repositories
- Consider using organization-level secrets for enterprise deployments
- The tool only reads code diffs and doesn't execute any code

## 📊 Performance Tips

1. **Use GPT-3.5-turbo** for faster, cheaper reviews (slightly lower quality)
2. **Limit max_comments** to reduce API calls
3. **Use specific ignore_patterns** to skip unnecessary files
4. **Disable unnecessary focus_areas** to speed up analysis
5. **Consider caching** for repeated PR updates (future feature)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PyGithub](https://github.com/PyGithub/PyGithub)
- LLM integration via [OpenAI](https://openai.com) and [Anthropic](https://anthropic.com)
- Inspired by various code review tools and AI assistants

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-code-reviewer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-code-reviewer/discussions)

---

Made with ❤️ by developers, for developers. Powered by AI 🤖
