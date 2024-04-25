torch-model-archiver \
    --model-name finroberta \
    --version "0.1" \
    --config-file model-config.yaml \
    --serialized-file ./distilroberta_raw/model.safetensors \
    --handler ./handler.py \
    --export-path ./model-store \
    --force