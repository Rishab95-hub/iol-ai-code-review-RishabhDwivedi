# Sample PR Testing Guide

This directory contains intentionally buggy code files for testing the AI Code Reviewer.

## Files with Intentional Issues

### buggy_user_service.py
Contains the following intentional issues:
- **Security**: SQL injection vulnerabilities, hardcoded credentials, weak password hashing (MD5)
- **Performance**: N+1 query problem, inefficient O(n^2) algorithm
- **Code Quality**: Missing error handling, global mutable state, unused methods
- **Best Practices**: Missing docstrings, poor resource management
- **Documentation**: Missing or inadequate comments

### buggy_api_handler.py
Contains the following intentional issues:
- **Security**: Command injection, insecure deserialization, hardcoded AWS keys, eval() usage
- **Security**: Disabled SSL verification, path traversal vulnerability
- **Security**: Weak random number generation, template injection
- **Code Quality**: Bare except clauses, silent failures, logging sensitive data
- **Best Practices**: Missing type hints, debug mode enabled, no rate limiting

## How to Test

1. Create a new branch:
   ```bash
   git checkout -b test-ai-review
   ```

2. Commit the buggy files:
   ```bash
   git add sample-pr/
   git commit -m "Add sample code with various issues"
   ```

3. Push and create a PR:
   ```bash
   git push origin test-ai-review
   ```

4. The AI Code Reviewer should automatically analyze the PR and post comments identifying the issues.

## Expected Review Comments

The AI reviewer should catch and comment on:
- 🔴 **Critical**: Hardcoded secrets, SQL injection, command injection
- 🟠 **Warning**: Weak hashing, N+1 queries, missing error handling
- 🟢 **Suggestion**: Missing docstrings, inefficient algorithms, code smells
