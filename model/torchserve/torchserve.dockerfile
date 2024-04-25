FROM pytorch/torchserve
COPY ./requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt
WORKDIR /home/model-server
# COPY ./model-store/* model-store/
COPY ./config.properties config.properties
ENTRYPOINT ["torchserve", "--model-store", "model-store", "--start", "--models",  "finroberta=finroberta.mar", "--ts-config config.properties", "--foreground"]