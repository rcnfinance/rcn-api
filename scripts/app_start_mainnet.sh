[ "$(docker ps -q)" ] && docker stop $(docker ps -aq)
[ "$(docker ps -aq)" ] && docker rm -f $(docker ps -aq)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate