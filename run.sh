#!/bin/bash

## SETUP VARIABLES

PATH_ROOT=$(pwd)
PATH_TO_SIM="$PATH_ROOT/demo/sim/"

MODE=$1


## STOP THE APP(S)

if [ "$MODE" == "stop" ]; then
    cd $PATH_TO_SIM && docker compose down --remove-orphans
    cd $PATH_ROOT && docker-compose down --remove-orphans
    exit 0
fi


## RUN THE APP(S)

if [ "$MODE" == "sim" ]; then
    echo "Running simulation..."
    cd $PATH_TO_SIM && docker compose up -d --build
    cd $PATH_ROOT
fi

echo "Running LogChain..."
docker-compose up -d --build
echo "LogChain running at https://localhost:8016"
echo "ntfy running at https://localhost:8047"


## OPEN THE APPS

sleep 5
wslview http://localhost:8047
sleep 3
wslview http://localhost:8016
