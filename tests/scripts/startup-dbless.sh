json-server-auth /kong/declarative/db.json &
# /usr/bin/kong-python-pluginserver --no-lua-style --plugins-directory /usr/local/kong/python/ &
# kong check /kong/declarative/kong.conf
# kong start --conf /kong/declarative/kong.conf
kong start

# Good request
curl --request GET \
  --url http://localhost:8000/anything \
  --header 'token: bWFpbEBuaXRpbmtoYW5uYS5jb206YmVzdFBhc3N3MHJk'

# Bad request
curl -i --request GET \
  --url http://localhost:8000/anything \
  --header 'token: bWFpbEBuaXRpbmtoYW5uYS5jb206d3JvbmdQYXNzdzByZA=='

python3 /kong/declarative/runIntegrationTest.py