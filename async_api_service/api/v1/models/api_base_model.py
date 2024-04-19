import orjson
from pydantic import BaseModel


def orjson_dumps(model_value, *, default):
    return orjson.dumps(model_value, default=default).decode()


class Base(BaseModel):
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
