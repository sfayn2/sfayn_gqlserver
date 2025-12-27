#!/usr/bin/env bash

# Exit immediately if a command fails
set -e

# --- Configuration ---
#HANDLER_FILE="../../ddd/order_management/entrypoints/lambda_handlers/lambda_handler_graphql.py"  # Your main python script

# Point this to the ROOT folder of your python package (where 'ddd' is)
SRC_ROOT="../../ddd"
BUILD_DIR="package_temp"           # Temp folder for staging
ZIP_NAME="lambda_handler_graphql.zip"   # Final output file

echo "Cleaning up..."
rm -rf "$BUILD_DIR" "$ZIP_NAME"
mkdir -p "$BUILD_DIR"

# 1. Install dependencies directly into the build directory root
# Use -t to specify the target folder
if [ -f "requirements_aws_localstack.txt" ]; then
    echo "Installing dependencies with uv..."
    # --system is often needed if you are not in an active venv
    uv run --active \
        uv pip install \
        -r requirements_aws_localstack.txt \
        --target "$BUILD_DIR" \
        --upgrade

fi


# 2. Copy the handler file to the root of the build directory
echo "Adding handler code..."
#cp -r "$HANDLER_FILE" "$BUILD_DIR/"
cp -r "$SRC_ROOT" "$BUILD_DIR/"

# 3. Create the ZIP from the contents of the build directory
# We 'cd' inside so the folders are not nested in the ZIP
echo "Creating zip: $ZIP_NAME..."
cd "$BUILD_DIR"
zip -r "../$ZIP_NAME" .
cd ..

echo "Done! Use $ZIP_NAME to deploy to LocalStack."

