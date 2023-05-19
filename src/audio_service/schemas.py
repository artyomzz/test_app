from pydantic import UUID4, BaseModel


class UserCreateIn(BaseModel):
    username: str


class UserCreateOut(BaseModel):
    id: UUID4
    access_token: UUID4

    class Config:
        orm_mode = True


class RecordCreateOut(BaseModel):
    url: str
