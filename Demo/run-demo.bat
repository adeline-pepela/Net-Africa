@echo off
REM ============================================
REM Continuous Quality Monitoring Demo
REM Windows Batch Script
REM ============================================

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║  Continuous Quality Monitoring for .NET AI Agents         ║
echo ║  Amazon Bedrock AgentCore Evaluations Demo               ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if dotnet is installed
where dotnet >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] .NET SDK not found. Please install .NET 8.0 or later.
    echo Download from: https://dotnet.microsoft.com/download
    pause
    exit /b 1
)

REM Display .NET version
echo [INFO] .NET Version:
dotnet --version
echo.

REM Create output directories
if not exist "traces" mkdir traces
if not exist "metrics" mkdir metrics
echo [INFO] Output directories created (if needed)
echo.

REM Restore dependencies
echo [INFO] Restoring dependencies...
dotnet restore
if %errorlevel% neq 0 (
    echo [ERROR] Failed to restore dependencies
    pause
    exit /b 1
)
echo.

REM Run the application
echo [INFO] Starting demo application...
echo [INFO] Choose a mode:
echo   1 = Interactive Chat (Local Development)
echo   2 = Batch Evaluation (CI/CD + Production)
echo   3 = Production Simulation
echo   4 = View Recent Results
echo.

dotnet run --configuration Release

echo.
echo [INFO] Demo completed
echo [INFO] Output files saved to:
echo   - traces/ (OpenTelemetry traces)
echo   - metrics/ (Evaluation results)
echo.
pause
