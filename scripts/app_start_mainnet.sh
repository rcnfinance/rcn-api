set -e
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate