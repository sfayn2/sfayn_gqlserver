#!/bin/bash

echo "Running AWS (LocalStack) Tests..."

# Get the absolute path of the directory where THIS script is located
export PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT
# Set the infrastructure type flag for your conftest.py switcher
export ORDER_MANAGEMENT_INFRA_TYPE="AWS" 

# Add this to your .sh files
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"
export AWS_REGION="us-east-1"
export DYNAMODB_TABLE_NAME="tntoms-tst-main-table"
export AWS_ENDPOINT_URL="http://localhost:4566"
export SKIP_JWT_VERIFY="true"


# Ensure LocalStack is running before proceeding (optional but recommended)
# Check if the port is open and if DynamoDB/Lambda are 'available'
HEALTH_CHECK=$(curl -s http://localhost:4566/_localstack/health)

if [[ $HEALTH_CHECK == *"available"* ]]; then
    echo "✅ LocalStack is healthy."
else
    echo "❌ LocalStack is not ready. Status: $HEALTH_CHECK"
    exit 1
fi



#uv run pytest "$PROJECT_ROOT/ddd/order_management/tests/e2e" -vv --tb=long -l -p no:django
#uv run pytest "$PROJECT_ROOT/ddd/order_management/tests/e2e" -p no:django
uv run pytest "$PROJECT_ROOT/ddd/order_management/tests/full_e2e" -p no:django
