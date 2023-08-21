FROM apache/spark-py:latest

USER root

RUN set -ex; \
    apt-get update; \
    apt-get install -y python3 python3-pip; \
    rm -rf /var/lib/apt/lists/*

RUN pip install pyspark

WORKDIR /usr/src/spark

COPY . .
