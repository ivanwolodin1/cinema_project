from pydantic import BaseModel, ConfigDict


class RoleDto(BaseModel):
    role: str


class RoleResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
