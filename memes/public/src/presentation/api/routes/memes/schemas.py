import datetime as dt
import typing as tp
import uuid

from fastapi import Body
from pydantic import BaseModel


class Paginator(BaseModel):
    offset: tp.Annotated[int, Body(ge=0)] = 0
    limit: tp.Annotated[int, Body(ge=0, le=100)] = 10


class PutMemeRequest(BaseModel):
    text: str


class MemeCreateRequest(PutMemeRequest):
    pass


class MemeUpdateRequest(PutMemeRequest):
    pass


class MemeDeleteRequest(BaseModel):
    meme_id: uuid.UUID


class MemeCreateResponse(BaseModel):
    meme_id: uuid.UUID


class MemeResponse(BaseModel):
    id: uuid.UUID
    image_url: str
    text: str
    created_at: dt.datetime


class MemeUpdateResponse(MemeResponse): ...


class MemeListResponse(BaseModel):
    items: list[MemeResponse]
