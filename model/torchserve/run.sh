docker run --rm -it \
    --name torchserve \
    -p 8080:8080 \
    -p 8081:8081 \
    -p 8082:8082 \
    -v model-store:/home/model-server/model-store \
    -v ./distilroberta_raw:/home/testing \
    torchserve 