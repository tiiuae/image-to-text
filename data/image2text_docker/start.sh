#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Please provide the jetson-containers path in SSD."
    echo "Usage: $0 <ssd_mounted_path>"
    exit 1
fi

# Store the input path
input_path="$1"

# Run the Docker command with the replaced path
sudo docker run --runtime nvidia -it --rm \
    --volume "${input_path}/data":/data \
    -p 5050:5000 \
    ghcr.io/tiiuae/image-to-text:latest

#    --network host \
#    image2text_app:latest
