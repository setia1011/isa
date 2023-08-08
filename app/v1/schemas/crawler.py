from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field, validator
from pydantic.dataclasses import dataclass

# config = ConfigDict(orm_mode=True, allow_population_by_field_name=True)

@dataclass
class Source(BaseModel):
    id: int
    source: str
    description: str
    site: str

@dataclass
class Url(BaseModel):
    id: int
    source_id: int
    crawled_at: datetime
    url: str
    status: str

@dataclass
class Urlx(BaseModel):
    id: int
    crawled_at: datetime
    url: str
    status: str
    source_id: int
    source_details: Source

@dataclass
class Urls(BaseModel):
    items: list[Urlx]
    total_pages: int
    total_items: int

@dataclass
class Contentx(BaseModel):
    id: int
    crawled_at: datetime
    author: str
    title: str
    label: str
    posted_at: str
    content: str
    url_id: int
    url_details: Url
    source_id: int
    source_details: Source

@dataclass
class Contents(BaseModel):
    items: list[Contentx]
    total_pages: int
    total_items: int