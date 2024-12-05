#!/bin/bash
set -e

# Function to install packages
install_packages() {
    echo "Updating package list..."
    sudo apt update

    echo "Installing build-essential and other required tools..."
    sudo apt install -y build-essential autoconf automake libtool pkg-config gifsicle

    echo "Installing NPM packages..."
    npm install --save-dev gifsicle optipng mozjpeg

    echo "Custom package installation complete."
}

rm -rf dist
rm -rf node_modules

echo "Installing dependencies..."

# Check the architecture
ARCH=$(uname -m)
echo "Detected ARM architecture: $ARCH"

# Check if the architecture is ARM
if [[ "$ARCH" == "armv7l" || "$ARCH" == "aarch64" ]]; then
    install_packages
fi

npm install --only=dev

echo "Running Gulp to build static files..."
npx gulp

echo "Static files generated in the dist folder."
