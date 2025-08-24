@echo off
REM Direct Ollama runner - bypasses all PATH issues

echo Starting Ollama directly...

REM Try standard location first
if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
    echo Found Ollama at standard location
    "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve
) else (
    REM Try Program Files
    if exist "%ProgramFiles%\Ollama\ollama.exe" (
        echo Found Ollama in Program Files
        "%ProgramFiles%\Ollama\ollama.exe" serve
    ) else (
        echo ERROR: Ollama not found!
        echo.
        echo Please install from: https://ollama.com/download/windows
        pause
    )
)
