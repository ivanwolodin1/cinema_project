FROM python:3.11

WORKDIR /tests

COPY functional/requirements.txt /tests/functional/requirements.txt
RUN pip install -r /tests/functional/requirements.txt --no-cache-dir

COPY . /tests/

CMD ["python3", "tests/functional/utils/wait_for_es.py"]
CMD ["python3", "tests/functional/utils/wait_for_redis.py"]

CMD ["sh", "-c", "pytest -v /tests/functional/src"]