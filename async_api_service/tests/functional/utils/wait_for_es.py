import time

import backoff
from elasticsearch import Elasticsearch
from tests.functional.settings import test_settings

TIMEOUT_VALUE = 300
SLEEP_VALUE = 30


@backoff.on_exception(
    backoff.expo, Exception, max_tries=test_settings.es_max_tries,
)
def wait_for_es():
    es_client = Elasticsearch(
        hosts=test_settings.es_host,
        request_timeout=TIMEOUT_VALUE,
        max_retries=10,
        retry_on_timeout=True,
    )
    while True:
        if es_client.ping():
            break
        time.sleep(SLEEP_VALUE)


if __name__ == '__main__':
    wait_for_es()
