FROM python:3.12-slim

ENV PYTHONUNBUFFERED true
ENV TZ UTC
WORKDIR /app
RUN apt-get update && apt-get -y upgrade

RUN pip install --upgrade pip
COPY backend/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY backend/ /app/

CMD celery -A worker.celery_worker worker --concurrency=$WORKER_CONCURRENCY --without-gossip -Q $QUEUE
