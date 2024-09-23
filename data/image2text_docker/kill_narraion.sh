#!/bin/bash

RUNDIR=$(pwd)

kill $(cat nats-server.pid)
kill $(voiceRecognition.pid)
kill $(cat piper.pid)
kill $(cat text2speech.pid)
kill $(cat image-to-text.pid)
kill $(cat cameraFetcher.pid)
