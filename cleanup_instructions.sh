kill $(ps aux | grep '[j]son-server' | awk '{print $2}')
docker rm -f kong-py-plugins
docker rm -f kong-database
docker network rm kong-net