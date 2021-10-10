#!/bin/bash

FRAMES_COUNT=""
INTERVAL=""

if [ xFALSE != x"$1" ]; then
   FRAMES_COUNT="--frames $1"
fi
if [ xFALSE != x"$2" ]; then
   INTERVAL="--interval $2"
fi

yes | gphoto2 --port "$(sh detect-camera.sh)" --capture-image-and-download $FRAMES_COUNT $INTERVAL
