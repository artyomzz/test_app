FROM python:3.10-slim
RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg

COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN chmod a+x scripts/run.sh
