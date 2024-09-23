#!/bin/bash

RUNDIR=$(pwd)

kill $(cat nats-server.pid)
nats-server -p 4223 -js &
echo $! > nats-server.pid

nats -s localhost:4223 kv add device-info
nats -s localhost:4223 kv put device-info manpack '{"device_type":"manpack", "device_alias": "AlphaOne"}'
nats -s localhost:4223 kv add current-mission

export DEVICE_ID=manpack
export NATS_SERVER_URL=nats://localhost:4223
export NATS_KEYVALUE_URL=nats://localhost:4223

cd voicerecognition
# make
kill $(voiceRecognition.pid)
./start.sh &
echo $! > $RUNDIR/voiceRecognition.pid
cd $RUNDIR

cd text-to-speech
kill $(cat piper.pid)
./piper.sh &
echo $! > $RUNDIR/piper.pid
kill $(cat text2speech.pid)
./start.sh &
echo $! > $RUNDIR/text2speech.pid
cd $RUNDIR

cd image-to-text/data/image2text_docker
# ./build.sh
kill $(echo image-to-text.pid)
./start $RUNDIR/image-to-text
echo $! > image-to-text.pid

cd CameraFetcher
# make
kill $(cat cameraFetcher.pid)
./cameraFetcher &
echo $! > $RUNDIR/CameraFetcher.pid
cd $RUNDIR
