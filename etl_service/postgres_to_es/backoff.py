import time
from functools import wraps
from typing import Iterable

from constants import EXCEPTION_ON_EXCEEDING_TRIES_LIMIT
from logger import logger


def backoff(
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 10,
    exceptions: Iterable = (Exception,),
    max_attempts: int = 10,
):
    """Функция, дающая сервисам передышку.

    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor)
    до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param exceptions: список исключений
    :param max_attempts: максимальное количество попыток
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            tries = 0
            while tries < max_attempts:
                timer = min(
                    border_sleep_time,
                    start_sleep_time * factor**tries,
                )
                if tries > 0:
                    time.sleep(timer)
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    tries += 1
                    logger.error(f'Backoff is working! {str(error)}')
            logger.error(EXCEPTION_ON_EXCEEDING_TRIES_LIMIT)
            raise Exception(EXCEPTION_ON_EXCEEDING_TRIES_LIMIT)

        return inner

    return func_wrapper
