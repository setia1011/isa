from fastapi import Depends
from sqlalchemy.orm import Session
from app.models import Urls, Contents, Sources


def insert_source(source: str, description: str, site: str, db: Session = Depends):
    data = Sources(source=source, description=description, site=site)
    return data

def insert_url(crawled_at: str, url: str, source_id: int, status: str, db: Session = Depends):
    data = Urls(crawled_at=crawled_at, url=url, source_id=source_id, status=status)
    return data

