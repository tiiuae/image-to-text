#!/bin/bash

sudo docker run --runtime nvidia -it --rm \
    -p 5050:5000 \
    ghcr.io/tiiuae/image-to-text:latest
