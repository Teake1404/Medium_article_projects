#!/bin/bash
cd /Users/shuqingke/Documents/ecommerce_mcp/ecommerce_mcp

# Completely isolate from Anaconda environment
unset CONDA_DEFAULT_ENV
unset CONDA_PREFIX
unset CONDA_PYTHON_EXE
unset CONDA_EXE

# Set clean PATH without Anaconda
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Activate the clean virtual environment
source ../.venv/bin/activate

# Run the MCP server with all arguments passed through
exec python mcp_server.py "$@" 