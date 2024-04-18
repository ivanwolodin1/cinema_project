from http import HTTPStatus

from api.v1.models.api_film_models import Genre
from fastapi import APIRouter, Depends, HTTPException
from services.genre_service import GenreService, get_genre_service

router = APIRouter()


@router.get(
    '/',
    response_model=list[Genre],
    summary='Список жанров',
    description='Список жанров',
    response_description='Список жанров с id и названием',
)
async def genres(
    genre_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    all_genres = await genre_service.get_all()
    if not all_genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genres not found',
        )
    return [Genre(**genre) for genre in all_genres]


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Информация о жанре',
    description='Информация о жанре',
    response_description='ID, название жанра',
)
async def genre_info(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_id(index='genres', doc_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genre not found',
        )
    return Genre(id=genre.id, name=genre.name)
