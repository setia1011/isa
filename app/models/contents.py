from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class Contents(Base):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True, index=True)
    crawled_at = Column(TIMESTAMP, nullable=False, index=True)
    label = Column(VARCHAR(500), index=True)
    author = Column(VARCHAR(500), index=True)
    posted_at = Column(VARCHAR(150), index=True)
    title = Column(VARCHAR(500), index=True)
    content = Column(TEXT)
    url_id = Column(Integer, ForeignKey('urls.id'), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False, index=True)

    ref_url = relationship('Urls', backref='contents')
    ref_source = relationship('Sources', backref='contents')