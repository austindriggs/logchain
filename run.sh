#!/bin/bash

# shut everything down from last time
cd tools/ && docker compose down --remove-orphans
cd ../ && docker-compose down --remove-orphans

# start everything back up
cd tools/ && docker-compose up -d --build
cd ../ && docker-compose up -d --build

# open app(s)
sleep 5
wslview http://localhost:8047
sleep 3
wslview http://localhost:8016
