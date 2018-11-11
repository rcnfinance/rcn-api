#!/usr/bin/env bash
cd /home/ubuntu/server/
ls -d -1 $PWD/**/*
docker-compose up -d --build --force-recreate
