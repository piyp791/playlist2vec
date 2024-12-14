#!/bin/bash
set -e

docker compose down --volumes

cd web-server
echo "Step 1: Installing dependencies and running Gulp..."
./build-static.sh

sudo rm -rf /usr/share/nginx/html/*

echo "Copying static files..."
sudo cp -r dist/* /usr/share/nginx/html/

cd ../

echo "Step 2: Building Docker image..."
docker compose build --no-cache

echo "Step 3: Starting Docker containers..."
docker compose up -d
