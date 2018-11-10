[ "$(docker ps -q)" ] && docker stop $(docker ps -aq)
[ "$(docker ps -aq)" ] && docker rm -f $(docker ps -aq)
docker-compose up -d --build