from pydantic import BaseModel, HttpUrl
from typing import List, Dict


class Chapter(BaseModel):
    number: str
    pages: List[HttpUrl]

class Manga(BaseModel):
    title: str
    author: str
    description: str
    cover: HttpUrl
    chapters: List[Chapter]

class SiteConfig(BaseModel):
    name: str
    base_url: HttpUrl
    downloads_dir: str
    site_url: HttpUrl
    ignore_existing_manga: bool
    ignore_existing_chapter: bool
    check_new_chapters: bool
    overwrite: bool
    selectors: Dict[str, str]

class Config(BaseModel):
    sites: List[SiteConfig]
