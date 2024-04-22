from pydantic import BaseModel


class UserCreate(BaseModel):
    password: str
    email: str
    role_id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    password: str
    email: str

    class Config:
        orm_mode = True


class UserAuthentication(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
