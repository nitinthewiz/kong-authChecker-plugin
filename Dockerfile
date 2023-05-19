FROM kong/kong-gateway:2.8.4.0
USER root

RUN apk update && \
    apk add python3 py3-pip python3-dev musl-dev libffi-dev gcc g++ file make
RUN PYTHONWARNINGS=ignore pip3 install kong-pdk requests
COPY /plugins /usr/local/kong/python/

# reset back the defaults
USER kong
STOPSIGNAL SIGQUIT
HEALTHCHECK --interval=10s --timeout=10s --retries=10 CMD kong health
CMD ["bash", "/kong/declarative/startup.sh"]