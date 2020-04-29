#!/bin/bash



FILE=/myFiles/READY
if test -f "$FILE"; then
	exit 0
else
	exit 1
fi
