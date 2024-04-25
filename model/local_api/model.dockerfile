# syntax = docker/dockerfile:experimental
FROM python:3.11-slim
COPY ./model/requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt
WORKDIR /opt/kamikaze_model
COPY ./model/main.py /opt/kamikaze_model/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]