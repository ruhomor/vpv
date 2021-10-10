#!/bin/bash

gphoto2 --auto-detect | grep Nikon | awk '{print $4}'
