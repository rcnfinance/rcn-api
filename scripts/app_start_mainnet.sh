docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker-compose up -d --build -f docker-compose.prod.yml