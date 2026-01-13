#!/bin/bash

echo "Running On-Prem (Django) Tests..."

# Get the absolute path of the directory where THIS script is located
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)


# Ensure the root is in PYTHONPATH so ddd is importable
export PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH

export ORDER_MANAGEMENT_INFRA_TYPE="ONPREM_DJANGO" 
export SECRET_KEY="local-testing-secret-key-123"

export DJANGO_SETTINGS_MODULE="sfayn_gqlserver.settings"

# Use the absolute path to the tests folder
# We use $PROJECT_ROOT/ddd/... instead of ../ddd/...
uv run pytest "$PROJECT_ROOT/ddd/order_management/tests" --ignore-glob="*aws*"
