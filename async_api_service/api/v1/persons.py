from http import HTTPStatus

from api.v1.models.api_film_models import FilmBase
from api.v1.models.api_person_models import Person
from api.v1.utils.paginated_params import PaginatedParams
from fastapi import APIRouter, Depends, HTTPException
from services.film_service import FilmService, get_film_service
from services.person_service import PersonService, get_person_service

router = APIRouter()


@router.get(
    '/search',
    response_model=list[Person],
    summary='Поиск персон',
    description='Поиск по персонам по запросу',
    response_description='Список персон с id, именем и ролью',
)
async def search_person(
    query: str = '',
    paginated_params: PaginatedParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person] | dict:

    if query is not None:
        persons = await person_service.search_person(
            query=query,
            page_number=paginated_params.page_number,
            page_size=paginated_params.page_size,
        )
        return [Person(**person) for person in persons]

    return {'err': 'specify request'}


@router.get(
    '/{person_id}',
    response_model=Person,
    summary='Информация о персоне по ID',
    description='Информация о персоне по ID',
    response_description='ID, полное имя, роль',
)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_by_id(index='persons', doc_id=person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='person not found',
        )
    return Person.parse_raw(person.json())


@router.get(
    '/{person_id}/film',
    response_model=list[FilmBase],
    summary='Информация о фильмах по персоне',
    description='Информация о фильмах по персоне - Id, title, imdb_rating',
    response_description='Id, title, imdb_rating',
)
async def movie_by_person(
    person_id: str, movies_service: FilmService = Depends(get_film_service),
) -> list[FilmBase]:
    films_by_person = await movies_service.get_films_by_person(
        person_id=person_id,
    )
    if not films_by_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='films_by_person not found',
        )
    return [FilmBase(**film) for film in films_by_person]
