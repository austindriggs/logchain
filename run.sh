#!/bin/bash

# shut everything down from last time
cd tools/ && docker compose down
cd ../ && docker-compose down

# start everything back up
cd tools/ && docker-compose up -d --build
cd ../ && docker-compose up -d --build
