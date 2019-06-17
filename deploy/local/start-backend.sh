#!/bin/bash

docker-compose up -d --force-recreate redis
docker-compose up -d --force-recreate manager
docker-compose up -d --force-recreate producer

