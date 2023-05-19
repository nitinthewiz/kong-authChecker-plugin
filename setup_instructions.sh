#!/usr/bin/env bash
docker build -t kong-py:0.1.0 .

docker network create kong-net

docker run -d --name kong-database \
  --network=kong-net \
  -p 5432:5432 \
  -e "POSTGRES_USER=kong" \
  -e "POSTGRES_DB=kong" \
  -e "POSTGRES_PASSWORD=kong" \
  postgres:13

docker run --rm --network=kong-net \
 -e "KONG_DATABASE=postgres" \
 -e "KONG_PG_HOST=kong-database" \
 -e "KONG_PG_PASSWORD=kong" \
 -e "KONG_PASSWORD=test" \
kong/kong-gateway:2.8.4.0 kong migrations bootstrap

docker run --rm --network=kong-net \
 -e "KONG_DATABASE=postgres" \
 -e "KONG_PG_HOST=kong-database" \
 -e "KONG_PG_PASSWORD=kong" \
 -e "KONG_PASSWORD=test" \
kong/kong-gateway:2.8.4.0 kong migrations up

docker run --rm --network=kong-net \
 -e "KONG_DATABASE=postgres" \
 -e "KONG_PG_HOST=kong-database" \
 -e "KONG_PG_PASSWORD=kong" \
 -e "KONG_PASSWORD=test" \
kong/kong-gateway:2.8.4.0 kong migrations finish

npm install -g express json-server json-server-auth
json-server-auth ./tests/scripts/db.json & 

# curl -i -X POST --url http://localhost:8001/services/httpbin-anything/plugins/ --data 'name=authChecker'
