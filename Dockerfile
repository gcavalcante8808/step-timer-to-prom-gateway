FROM python:3-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    make && \
    apt-get clean && \
    rm -rf /tmp/* /var/lib/apt/lists/*

WORKDIR /usr/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
