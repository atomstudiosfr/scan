FROM python:3.12-slim

ENV PYTHONUNBUFFERED true
ENV TZ UTC
WORKDIR /app
RUN apt-get update && apt-get -y upgrade

RUN pip install --upgrade pip
COPY backend/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY backend/ /app/

CMD uvicorn api.main:create_app --factory --host 0.0.0.0 --port 5002 --use-colors --proxy-headers --forwarded-allow-ips '*' --loop uvloop --http httptools
