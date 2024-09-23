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
    --volume /tmp/argus_socket:/tmp/argus_socket \
    --volume /etc/enctune.conf:/etc/enctune.conf \
    --volume /etc/nv_tegra_release:/etc/nv_tegra_release \
    --volume /tmp/nv_jetson_model:/tmp/nv_jetson_model \
    --volume /var/run/dbus:/var/run/dbus \
    --volume /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "${input_path}/data":/data \
    --device /dev/snd \
    --device /dev/bus/usb \
    -e DISPLAY=:0 \
    -v /tmp/.X11-unix/:/tmp/.X11-unix \
    -v /tmp/.docker.xauth:/tmp/.docker.xauth \
    -e XAUTHORITY=/tmp/.docker.xauth \
    --device /dev/i2c-0 \
    --device /dev/i2c-1 \
    --device /dev/i2c-2 \
    --device /dev/i2c-3 \
    --device /dev/i2c-4 \
    --device /dev/i2c-5 \
    --device /dev/i2c-6 \
    --device /dev/i2c-7 \
    --device /dev/i2c-8 \
    --device /dev/i2c-9 \
    -v /run/jtop.sock:/run/jtop.sock \
    -p 5050:5000 \
    ghcr.io/tiiuae/image-to-text:latest

#    --network host \
#    image2text_app:latest
