from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import db_session
from app.v1.services import crawler as crawler_services
from app.v1.schemas import crawler as crawler_schema, simple as simple_schema
from app.v1.crawlers.cnbc_indonesia import url_crawler as url_crawler_cnn_indonesia
from app.v1.crawlers.cnbc_indonesia import content_crawler as content_crawler_cnn_indonesia


router = APIRouter()

@router.get('/crawler-cnn-indonesia', response_model=simple_schema.Simple)
async def crawler_cnn_indonesia(keywords: str = 'beacukai', date: str = '', pages: int = 2, db: Session = Depends(db_session)):
    try:
        # url_crawler_cnn_indonesia.url_crawler(keywords=keywords, date=date, pages=pages, db=db)
        content_crawler_cnn_indonesia.content_crawler(db=db)
        return {"detail": "Succeeded"}
    except Exception as e:
        raise
        return {"detail": "Failed"}

@router.get('/urls', response_model=crawler_schema.Urls, description='Get all urls with pagination')
async def urls(source_id: int = '', page: int = 1, per_page: int = 10, db: Session = Depends(db_session)):
    try:
        import math
        offset = (page-1) * per_page
        urls = crawler_services.urls(source_id=source_id, page=offset, per_page=per_page, db=db)
        urls_count = crawler_services.urls_count(source_id=source_id, db=db)
        data = {}
        data['items'] = urls
        data['total_pages'] = math.ceil(urls_count/per_page)
        data['total_items'] = urls_count
        db.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=422, detail='Failed')

@router.get('/contents', response_model=crawler_schema.Contents, description='Get all contents with pagination')
async def contents(keywords: str = '', page: int = 1, per_page: int = 10, db: Session = Depends(db_session)):
    try:
        import math
        offset = (page-1) * per_page
        contents = crawler_services.contents(keywords=keywords, page=offset, per_page=per_page, db=db)
        contents_count = crawler_services.contents_count(keywords=keywords, db=db)
        data = {}
        data['items'] = contents
        data['total_pages'] = math.ceil(contents_count/per_page)
        data['total_items'] = contents_count
        db.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=422, detail='Failed')