#!/usr/bin/env bash
cd /home/ubuntu/server/
ls -d -1 $PWD/**/*
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate