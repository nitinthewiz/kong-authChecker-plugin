docker build -f $(pwd)/tests/scripts/Dockerfile.test -t kong-py-test:0.1.0 .

docker network create kong-net

docker run --name kong-authChecker-plugin-dbless \
--network=kong-net \
--link kong-database:kong-database \
--mount type=bind,source=$(pwd)/plugins,destination=/usr/local/kong/python/ \
--mount type=bind,source=$(pwd)/tests/scripts,destination=/kong/declarative/ \
-e "KONG_DATABASE=off" \
-e "KONG_DECLARATIVE_CONFIG=/kong/declarative/kong.yml" \
-e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
-e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
-e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
-e "KONG_PLUGINS=bundled,authChecker" \
-e "KONG_PLUGINSERVER_NAMES=python-plugin" \
-e "KONG_PLUGINSERVER_PYTHON_PLUGIN_SOCKET=/usr/local/kong/python_pluginserver.sock" \
-e "KONG_PLUGINSERVER_PYTHON_PLUGIN_START_CMD=/usr/bin/kong-python-pluginserver --no-lua-style --plugins-directory /usr/local/kong/python/" \
-e "KONG_PLUGINSERVER_PYTHON_PLUGIN_QUERY_CMD=/usr/bin/kong-python-pluginserver --no-lua-style --plugins-directory /usr/local/kong/python/ --dump-all-plugins" \
-e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
 kong-py-test:0.1.0

docker rm -f kong-authChecker-plugin-dbless
docker network rm kong-net