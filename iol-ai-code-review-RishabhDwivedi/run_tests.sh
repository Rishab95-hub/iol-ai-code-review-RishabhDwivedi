#!/bin/bash
# Linux/Mac bash script to run the AI Code Reviewer test suite

set -e

echo "============================================================"
echo " AI Code Reviewer - Test Runner"
echo "============================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "tests/test_script.py" ]; then
    echo "ERROR: test_script.py not found"
    echo "Please run this script from the ai-code-reviewer root directory"
    exit 1
fi

echo "Step 1: Installing dependencies..."
echo
pip3 install -q -r requirements.txt || {
    echo "ERROR: Failed to install dependencies"
    exit 1
}

echo
echo "Step 2: Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Please edit .env file and add your API keys"
    echo "Then run this script again"
    echo
    echo "Edit .env now? (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        ${EDITOR:-nano} .env
    fi
    exit 0
fi

echo
echo "Step 3: Running tests..."
echo
python3 tests/test_script.py

if [ $? -eq 0 ]; then
    echo
    echo "============================================================"
    echo " Tests PASSED - System is ready!"
    echo "============================================================"
    echo
    echo "Next steps:"
    echo "1. Push this code to your GitHub repository"
    echo "2. Add OPENAI_API_KEY to repository secrets"
    echo "3. Create a test PR to see the AI reviewer in action"
    echo
    echo "See QUICKSTART.md for detailed instructions"
    echo
else
    echo
    echo "============================================================"
    echo " Tests FAILED - Please fix the issues above"
    echo "============================================================"
    exit 1
fi
