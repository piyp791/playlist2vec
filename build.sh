#!/bin/bash
set -e

# Function to download and copy static resources
download_resources() {
    local resource_type=$1
    local search_index_file=$2
    local database_file=$3

    echo "Downloading ${resource_type} static resources..."
    if [ "$resource_type" = "mini" ]; then
        SEARCH_INDEX_DOWNLOAD_LINK="https://filedn.com/lh14Jds6qK88cdaUD0PxR5j/playlist2vec/playlist_tree_mini.usearch"
        DATABASE_DOWNLOAD_LINK="https://filedn.com/lh14Jds6qK88cdaUD0PxR5j/playlist2vec/playlist2vec_mini.db"
    else
        SEARCH_INDEX_DOWNLOAD_LINK="https://filedn.com/lh14Jds6qK88cdaUD0PxR5j/playlist2vec/playlist_tree.usearch"
        DATABASE_DOWNLOAD_LINK="https://filedn.com/lh14Jds6qK88cdaUD0PxR5j/playlist2vec/playlist2vec.db"
    fi
    wget "$SEARCH_INDEX_DOWNLOAD_LINK" -O "$search_index_file"
    wget "$DATABASE_DOWNLOAD_LINK" -O "$database_file"

    cp "$search_index_file" search-service/src/
    cp "$database_file" search-service/src/
    cp "$database_file" autocomplete-service/src/

    echo "Files copied to API folders. Cleaning up downloaded files..."
    rm "$search_index_file" "$database_file"
}

# Clean up previous Docker volumes
docker compose down --volumes

# Read the value of IS_MINI from the .env file
IS_MINI=$(grep -E '^IS_MINI=' .env | cut -d '=' -f2)

# Check for static resources based on the IS_MINI environment variable
if [ "$IS_MINI" = "true" ]; then
    if [ -f search-service/src/playlist_tree_mini.usearch ] && [ -f search-service/src/playlist2vec_mini.db ] && [ -f autocomplete-service/src/playlist2vec_mini.db ]; then
        echo "Mini static resources already exist in the API folders. Skipping download..."
    else
        download_resources "mini" "playlist_tree_mini.usearch" "playlist2vec_mini.db"
    fi
else
    if [ -f search-service/src/playlist_tree.usearch ] && [ -f search-service/src/playlist2vec.db ] && [ -f autocomplete-service/src/playlist2vec.db ]; then
        echo "Full static resources already exist in the API folders. Skipping download..."
    else
        download_resources "full" "playlist_tree.usearch" "playlist2vec.db"
    fi
fi

# Setup Docker registry
echo "Step 2: Setting up Docker registry..."
docker volume create registry-data
docker run -d -p 5000:5000 --restart always --name registry -v registry-data:/var/lib/registry registry:2

# Build and deploy Docker image
echo "Step 3: Building Docker image..."
docker compose build --no-cache

# Push Docker images to the registry
echo "Step 4: Pushing Docker images to the registry..."
docker image push localhost:5000/autocomplete-image:latest
docker image push localhost:5000/search-image:latest
docker image push localhost:5000/web-server-image:latest

