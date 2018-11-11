#!/usr/bin/env bash
echo "Stoping container"
[ "$(docker ps -q)" ] && docker stop $(docker ps -aq) || true
echo "Removing container"
[ "$(docker ps -aq)" ] && docker rm -f $(docker ps -aq) || true
exit 0