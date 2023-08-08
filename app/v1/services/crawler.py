from fastapi import Depends
from sqlalchemy.orm import Session, selectinload, lazyload, joinedload, subqueryload
from app.models import Urls, Sources, Contents
from app.v1.schemas import crawler as crawler_schema

def urls_count(source_id: int, db: Session = Depends):
    data = db.query(Urls).filter(Urls.source_id == source_id).count()
    return data

def urls(source_id: int, page: int, per_page: int, db: Session = Depends):
    data = db.query(Urls).options(
        selectinload(Urls.ref_source)).filter(Urls.source_id == source_id).limit(per_page).offset(page).all()
    items = []
    for i in data:
        items.append({
            'id': i.id,
            'url': i.url,
            'source_id': i.source_id,
            'source_details': {
                'id': i.ref_source.id,
                'source': i.ref_source.source,
                'description': i.ref_source.description,
                'site': i.ref_source.site
            },
            'crawled_at': i.crawled_at,
            'status': i.status
        })
    return items

def contents_count(keywords: str, db: Session = Depends):
    data = db.query(Contents).filter(Contents.content.like('%{0}%'.format(keywords))).count()
    return data

def contents(keywords: str, page: int, per_page: int, db: Session = Depends):
    data = db.query(Contents).options(
        selectinload(Contents.ref_source), 
        selectinload(Contents.ref_url)).filter(Contents.content.like('%{0}%'.format(keywords))).limit(per_page).offset(page).all()
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
                "id": i.ref_url.id,
                "source_id": i.ref_url.source_id,
                "status": i.ref_url.status,
                "crawled_at": i.ref_url.crawled_at,
                "url": i.ref_url.url
            },
            'source_id': i.source_id,
            'source_details': {
                'id': i.ref_source.id,
                'source': i.ref_source.source,
                'description': i.ref_source.description,
                'site': i.ref_source.site
            }
        })
    return items