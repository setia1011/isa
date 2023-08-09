from fastapi import Depends
from sqlalchemy.orm import Session, selectinload, lazyload, joinedload, subqueryload
from app.models import Url, Source, Content
from app.v1.schemas import crawler as crawler_schema
from typing import Optional


def urls_count(status: str, source_id: int, db: Session = Depends):
    data = db.query(Url).filter(Url.source_id == source_id).filter(Url.status == status).count()
    return data

def urls(status: str, source_id: int, page: Optional[int] = None, per_page: int = 10, db: Session = Depends):
    data = db.query(Url).options(selectinload(Url.source)).\
        filter(Url.source_id == source_id).filter(Url.status == status).\
            limit(per_page).offset(page).all()
    items = []
    for i in data:
        items.append({
            'id': i.id,
            'url': i.url,
            'source_id': i.source_id,
            'source_details': {
                'id': i.source.id,
                'source': i.source.source,
                'description': i.source.description,
                'site': i.source.site
            },
            'crawled_at': i.crawled_at,
            'status': i.status
        })
    return items

def contents_count(keywords: str, db: Session = Depends):
    data = db.query(Content).filter(Content.content.like('%{0}%'.format(keywords))).count()
    return data

def contents(keywords: str, page: int, per_page: int, db: Session = Depends):
    data = db.query(Content).options(
        selectinload(Content.source), 
        selectinload(Content.url)).filter(Content.content.like('%{0}%'.format(keywords))).limit(per_page).offset(page).all()
    items = []
    for i in data:
        items.append({
            "id": i.id,
            "crawled_at": i.crawled_at,
            "author": i.author,
            "title": i.title,
            "label": i.label,
            "posted_at": i.posted_at,
            "content": i.content,
            "url_id": i.url_id,
            "url_details": {
                "id": i.url.id,
                "source_id": i.url.source_id,
                "status": i.url.status,
                "crawled_at": i.url.crawled_at,
                "url": i.url.url
            },
            'source_id': i.source_id,
            'source_details': {
                'id': i.source.id,
                'source': i.source.source,
                'description': i.source.description,
                'site': i.source.site
            }
        })
    return items