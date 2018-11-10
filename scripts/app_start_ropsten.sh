[ "$(docker ps -q)" ] && docker stop $(docker ps -q)
[ "$(docker ps -aq)" ] && docker rm -f $(docker ps -aq)
docker-compose up -d --build --force-recreate