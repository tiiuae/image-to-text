#!/bin/bash

docker run --network=host --privileged -e DEVICE_ID=a2a049d4b2044b918 -e NATS_SERVER_HOST=127.0.0.1 -e NATS_SERVER_PORT=4223 -e PIPER_SERVER_HOST=127.0.0.1 -e PIPER_SERVER_PORT=5000 ghcr.io/tiiuae/manpack-tts-handler:sha-092e8a9
