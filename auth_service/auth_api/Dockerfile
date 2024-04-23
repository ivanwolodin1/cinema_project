FROM python:3.11

WORKDIR /auth_api

COPY requirements.txt .

RUN apt-get update && \
    apt-get -y install postgresql-client && \
    pip install -r requirements.txt --no-cache-dir

COPY .. .

RUN chmod +x entrypoint.sh

CMD ["sh", "entrypoint.sh"]
