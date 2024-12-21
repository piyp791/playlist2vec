#!/bin/bash
set -e

# Build static files
cd web-server
echo "Step 1: Installing dependencies and running Gulp..."
./build-static.sh

# Clear previous static files
sudo rm -rf /usr/share/nginx/html/*

# Copy new static files
echo "Copying static files..."
sudo cp -r dist/* /usr/share/nginx/html/

cd ../

echo "Step 3: Deploying docker stack..."
# docker compose up -d
docker stack config -c docker-compose.yaml | docker stack deploy -c - playlist2vec_stack
# docker stack deploy -c docker-compose.yaml playlist2vec_stack
