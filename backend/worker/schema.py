import enum
from datetime import datetime

from pydantic import BaseModel


class Provider(enum.StrEnum):
    ASURA_TOON = "ASURA_TOON"


class Chapter(BaseModel):
    number: float = -1
    href: str = ''
    images: list[str] = []

    class Config:
        validate_assignment = True


class Book(BaseModel):
    name: str = ''
    href: str = ''
    author: str = ''
    chapters: list[Chapter] = []
    last_updated: datetime = None
    provider: Provider = None

    class Config:
        validate_assignment = True

    def get_book_name_formatted(self):
        return self.name.lower().replace(' ', '-')

