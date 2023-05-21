json-server-auth /kong/declarative/db.json &
# /usr/bin/kong-python-pluginserver --no-lua-style --plugins-directory /usr/local/kong/python/ &
# kong check /kong/declarative/kong.conf
# kong start --conf /kong/declarative/kong.conf

echo "Starting kong with &"
kong start &

echo "Sleeping for 10 seconds to ensure kong is up. Ideally, this should happen via a check on the Kong admin API or docker output."
sleep 10

python3 /kong/declarative/run_integration_test.py || { echo "run_integration_test failed" && exit 1; }