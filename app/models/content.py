from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True, index=True)
    crawled_at = Column(TIMESTAMP, nullable=False, index=True)
    label = Column(VARCHAR(500), index=True)
    author = Column(VARCHAR(500), index=True)
    posted_at = Column(VARCHAR(150), index=True)
    title = Column(VARCHAR(500), index=True)
    content = Column(TEXT)
    url_id = Column(Integer, ForeignKey('url.id'), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False, index=True)

    url = relationship('Url', backref='content_url_reference')
    source = relationship('Source', backref='content_source_reference')