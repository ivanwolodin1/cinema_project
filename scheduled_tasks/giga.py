import re
from typing import Union

from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from langchain_core.tools import tool
import json

PROMPT_FILM_COUNT = 30
PROMPT_FORMAT_DIRECTIVE = "!в формате json"
PROMPT_COUNT = 5
FILM_COUNT = 10
AUTH = "YjRiMWFhMTktZDNlYS00ZDk5LWFmZjQtMTRjMjU2ZmZlNmZkOjczYmQyMjY3LTkxMjktNDIzMS1hZGEzLTc4OWM1NWI5MTI2MQ=="


def check_answer(answer: str, count: int) -> Union[bool, str]:
    """Проверяет валидность Json, возвращает список существующих фильмов"""
    try:
        answer_json = json.loads(re.sub(r"\n", "", answer.content))

        valid_films = []
        for film in answer_json:
            valid_films.append(film.get('title'))

        return valid_films

    except:
        return False


giga = GigaChat(credentials=AUTH,
                model='GigaChat:latest',
                verify_ssl_certs=False
                )

llm_with_tools = giga.bind()


def get_suggestion(like_films_prompt) -> list:

    msgs = [SystemMessage(
        content='Ты рекомендательный сервис, отдавай рекомендуемый список в json формате,\
            со структурой где поле title - наименование фильма.'
    ), HumanMessage(
        content=like_films_prompt
    )]

    answer = giga(msgs)
    print(f'answer={answer}')
    msgs.append(answer)

    films = []
    for _ in range(PROMPT_COUNT):
        check_result = check_answer(answer, FILM_COUNT)
        if check_result is False:
            msgs.append(HumanMessage(content='Исправь свой ответ на корректный JSON формат.'))
            answer = giga(msgs)
            msgs.append(answer)
        else:
            films += check_result
            if len(films) < FILM_COUNT:
                msgs.append(
                    HumanMessage(
                        content=f' Выведи еще список из {PROMPT_FILM_COUNT} рекомендуемых фильмов,\
                        фильмы из прошлого сообщения не выводи. {PROMPT_FORMAT_DIRECTIVE}. Название фильмов выводи на английском языке'
                    )
                )
                answer = giga(msgs)
                msgs.append(answer)
            else:
                break

    return films
