import time

import backoff
import redis
from tests.functional.settings import test_settings


@backoff.on_exception(
    backoff.expo, Exception, max_tries=test_settings.redis_max_tries,
)
def wait_for_redis():
    while True:
        try:
            redis_obj = redis.StrictRedis(test_settings.redis_host)
            redis_obj.ping()
            break
        except redis.ConnectionError:
            time.sleep(5)


if __name__ == '__main__':
    wait_for_redis()
