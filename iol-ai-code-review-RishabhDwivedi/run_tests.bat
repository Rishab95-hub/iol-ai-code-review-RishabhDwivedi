@echo off
REM Windows batch script to run the AI Code Reviewer test suite

echo ============================================================
echo  AI Code Reviewer - Test Runner
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "tests\test_script.py" (
    echo ERROR: test_script.py not found
    echo Please run this script from the ai-code-reviewer root directory
    pause
    exit /b 1
)

echo Step 1: Installing dependencies...
echo.
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Checking for .env file...
if not exist ".env" (
    echo WARNING: .env file not found
    echo Creating from .env.example...
    copy .env.example .env >nul
    echo.
    echo IMPORTANT: Please edit .env file and add your API keys
    echo Then run this script again
    echo.
    notepad .env
    pause
    exit /b 0
)

echo.
echo Step 3: Running tests...
echo.
python tests\test_script.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo  Tests FAILED - Please fix the issues above
    echo ============================================================
    pause
    exit /b 1
) else (
    echo.
    echo ============================================================
    echo  Tests PASSED - System is ready!
    echo ============================================================
    echo.
    echo Next steps:
    echo 1. Push this code to your GitHub repository
    echo 2. Add OPENAI_API_KEY to repository secrets
    echo 3. Create a test PR to see the AI reviewer in action
    echo.
    echo See QUICKSTART.md for detailed instructions
    echo.
    pause
    exit /b 0
)
