kong config db_import /kong/declarative/kong.yml
kong check /kong/declarative/kong.conf
kong start --conf /kong/declarative/kong.conf