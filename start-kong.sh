docker run -d --name kong-py-plugins \
--network=kong-net \
--link kong-database:kong-database \
--mount type=bind,source=$(pwd)/plugins,destination=/usr/local/kong/python/ \
-v "$(pwd):/kong/declarative/" \
-e "KONG_DATABASE=postgres" \
-e "KONG_PG_HOST=kong-database" \
-e "KONG_PG_USER=kong" \
-e "KONG_PG_PASSWORD=kong" \
-e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
-e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
-e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
-e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
-e "KONG_PLUGINS=bundled,
        authChecker" \
-e "KONG_PLUGINSERVER_NAMES=python-plugin" \
-e "KONG_PLUGINSERVER_PYTHON_PLUGIN_SOCKET=/usr/local/kong/python_pluginserver.sock" \
-e "KONG_PLUGINSERVER_PYTHON_PLUGIN_START_CMD=/usr/bin/kong-python-pluginserver --no-lua-style --plugins-directory /usr/local/kong/python/" \
-e "KONG_PLUGINSERVER_PYTHON_PLUGIN_QUERY_CMD=/usr/bin/kong-python-pluginserver --no-lua-style --plugins-directory /usr/local/kong/python/ --dump-all-plugins" \
-e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
-e KONG_LICENSE_DATA \
-p 8003:8000 \
-p 8443:8443 \
-p 8001:8001 \
-p 8002:8002 \
-p 8444:8444 \
 kong-py:0.1.0

echo "see logs 'docker logs kong-py-plugins -f'"