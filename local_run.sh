docker-compose down -v
docker-compose -f docker-compose.yml -f docker-compose.override.test.yml up -d --build

