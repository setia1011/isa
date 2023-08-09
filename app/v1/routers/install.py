import pandas as pd
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database import db_session
from app.core.config import settings
from app.v1.services import install as install_service
from app.v1.schemas import simple as simple_schema
import alembic.config
import mysql.connector


router = APIRouter()

@router.get("/install/", response_model=simple_schema.Simple, status_code=status.HTTP_200_OK)
async def install(db: Session = Depends(db_session)):
    try:
        # Create database
        dataBase = mysql.connector.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWORD
        )
        # preparing a cursor object
        cursorObject = dataBase.cursor()
        # creating database
        cursorObject.execute("CREATE DATABASE IF NOT EXISTS db_isa CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")

        # setup table schemas
        t = [('revision', '--autogenerate'), ('upgrade', 'head')]
        for i in range(len(t)):
            alembicArgs = [
                '--raiseerr',
                t[i][0], t[i][1],
            ]
            alembic.config.main(argv=alembicArgs)

        # Insert crawler sources
        file_sources = settings.ROOT_PATH + "/app/v1/data/crawler_sources.csv"
        df_sources = pd.read_csv(file_sources, usecols=["source","description","site"])
        for i, val in df_sources.iterrows():
            sources = install_service.insert_source(
                source=val['source'],
                description=val['description'],
                site=val['site'],
                db=db)
            db.add(sources)
            db.commit()
            db.refresh(sources)
        db.close()
        return {"detail": "The system is ready!"}
    except Exception as e:
        raise
        raise HTTPException(status_code=422, detail='Failed')
