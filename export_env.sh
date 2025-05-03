#!/bin/bash
# export_env.sh - Helper script to export environment variables from .env

# Check if the script is being sourced
(return 0 2>/dev/null) && sourced=true || sourced=false

if [ "$sourced" = false ]; then
    echo "❌ Error: This script needs to be sourced, not executed"
    echo "  Please run: source ./export_env.sh"
    echo "  This will ensure environment variables are available in your current shell"
    exit 1
fi

echo "🔐 Exporting environment variables from .env"

if [ ! -f .env ]; then
    echo "❌ Error: .env file not found in current directory"
    echo "  Please create a .env file with your API keys"
    return 1
fi

# Export all variables from .env file
set -a  # automatically export all variables
source .env
set +a  # stop automatically exporting

# Verify the keys were exported
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OPENAI_API_KEY successfully exported (${#OPENAI_API_KEY} characters)"
else
    echo "⚠️ Warning: OPENAI_API_KEY not found in .env file"
fi

if [ -n "$EXA_API_KEY" ]; then
    echo "✅ EXA_API_KEY successfully exported (${#EXA_API_KEY} characters)"
else
    echo "⚠️ Warning: EXA_API_KEY not found in .env file"
fi

# Print help message
echo ""
echo "🚀 You can now run the learning agent with:"
echo "  make run_openrouter  # Use OpenRouter models"
echo "  make run             # Use local Ollama models"
echo ""
echo "Note: These variables are only exported in the current shell session."
echo "To permanently add them, add them to your shell profile." 