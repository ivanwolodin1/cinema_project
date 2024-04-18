import orjson
from pydantic import BaseModel


def orjson_dumps(value_model, *, default):
    return orjson.dumps(value_model, default=default).decode()


class Base(BaseModel):
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
