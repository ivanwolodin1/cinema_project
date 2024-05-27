FROM python:3.11

WORKDIR /like_api

COPY requirements.txt .

RUN apt-get update && \
    apt-get -y install postgresql-client && \
    pip install -r requirements.txt --no-cache-dir

COPY .. .
CMD ["python", "main.py"]