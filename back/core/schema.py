from typing import List

from pydantic import BaseModel


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = None


class Chapter(BaseModel):
    title: str
    pages: List[str]


class Manga(BaseModel):
    title: str
    author: str
    description: str
    cover: str
    chapters: List[Chapter]
