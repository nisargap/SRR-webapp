\#!/bin/sh

cd /home/pi/Documents

rm -f wifite.log

timeout 5 bash -c "tee>(sudo wifite)|tee -a firstRun.txt"

timeout 10s

echo

echo

timeout 120 bash -c "tee>(sudo wifite -i wlan0 -e retrievers)|tee -a wifite.log"
