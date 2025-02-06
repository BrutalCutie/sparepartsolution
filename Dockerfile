FROM python:3.12

WORKDIR /app

COPY . /app

#RUN apt-get update && \
#    apt-get install -y gcc libpq-dev && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/* && \
#    pip install -r requirements.txt --no-cache-dir

RUN apt-get update && \
    pip install -r requirements.txt
