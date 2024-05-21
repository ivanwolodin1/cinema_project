from http import HTTPStatus

from api.v1.models.api_film_models import Film, FilmBase, EsMovie
from api.v1.utils.paginated_params import PaginatedParams
from core.auth_validator import auth_required
from fastapi import APIRouter, Depends, Header, HTTPException
from services.film_service import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/',
    response_model=list[FilmBase],
    summary='Список фильмов',
    description='Список фильмов с пагинацией, фильтрацией по жанрам и сортировкой по году или рейтингу',
    response_description='Список фильмов с id, названием и рейтингом',
)
@auth_required
async def get_films(
    authorization_header: str = Header(None),
    paginated_params: PaginatedParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmBase]:
    popular_films = await film_service.get_all(
        page_number=paginated_params.page_number,
        page_size=paginated_params.page_size,
    )
    return [FilmBase(**film.dict()) for film in popular_films]


@router.get(
    '/search',
    response_model=list[FilmBase],
    summary='Поиск фильмов',
    description='Поиск по фильмам по запросу',
    response_description='Список фильмов с id, названием, рейтингом',
)
async def search_films(
    query: str = '',
    genre_id: str = '',
    paginated_params: PaginatedParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
) -> list[FilmBase]:
    if genre_id:
        films = await film_service.get_popular_movies_in_genre(
            genre_id=genre_id,
        )
        return [FilmBase(**film) for film in films]

    elif query:
        films = await film_service.search_movie(
            query=query,
            page_number=paginated_params.page_number,
            page_size=paginated_params.page_size,
        )
        return [FilmBase(**film) for film in films]
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='specify request',
    )


@router.get(
    '/{film_id}',
    response_model=Film,
    summary='Информация о фильме по ID',
    description='Полная информация о фильме по ID',
    response_description='ID, название, описание, жанры, рейтинг, список участников',
)
# @auth_required
async def film_details(
    # authorization_header: str = Header(None),
    film_id: str = '',
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_by_id(index='movies', doc_id=film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='film not found',
        )
    return Film.parse_raw(film.json())


@router.post(
    '/find_intersection',
    summary='Возвращает пересечение между поданным списком фильмов и списком в нашем ES',
    # response_model=list[EsMovie],
)
async def find_intersection(
    movies_list: list[str],
    film_service: FilmService = Depends(get_film_service),
):
    movies_intercepted = await film_service.get_movies_interception(index='movies', movies=movies_list)
    return {
        'data': movies_intercepted,
    }
