#!/bin/bash

# ============================================
# Continuous Quality Monitoring Demo
# Linux/Mac Bash Script
# ============================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║  Continuous Quality Monitoring for .NET AI Agents         ║"
echo "║  Amazon Bedrock AgentCore Evaluations Demo               ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if dotnet is installed
if ! command -v dotnet &> /dev/null; then
    echo "[ERROR] .NET SDK not found. Please install .NET 8.0 or later."
    echo "Download from: https://dotnet.microsoft.com/download"
    exit 1
fi

# Display .NET version
echo "[INFO] .NET Version:"
dotnet --version
echo ""

# Create output directories
mkdir -p traces
mkdir -p metrics
echo "[INFO] Output directories created (if needed)"
echo ""

# Restore dependencies
echo "[INFO] Restoring dependencies..."
dotnet restore
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to restore dependencies"
    exit 1
fi
echo ""

# Run the application
echo "[INFO] Starting demo application..."
echo "[INFO] Choose a mode:"
echo "   1 = Interactive Chat (Local Development)"
echo "   2 = Batch Evaluation (CI/CD + Production)"
echo "   3 = Production Simulation"
echo "   4 = View Recent Results"
echo ""

dotnet run --configuration Release

echo ""
echo "[INFO] Demo completed"
echo "[INFO] Output files saved to:"
echo "   - traces/ (OpenTelemetry traces)"
echo "   - metrics/ (Evaluation results)"
echo ""
