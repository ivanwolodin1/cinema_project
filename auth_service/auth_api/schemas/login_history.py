from datetime import datetime

from pydantic import BaseModel


class LoginHistoryDto(BaseModel):
    device: str
    login_at: datetime

    class Config:
        orm_mode = True
