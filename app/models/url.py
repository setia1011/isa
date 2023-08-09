from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Enum, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True, index=True)
    crawled_at = Column(TIMESTAMP, nullable=False, index=True)
    url = Column(VARCHAR(500), unique=True, index=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False, index=True)
    status = Column(Enum('new','failed','crawled'), nullable=False, index=True)
    
    source = relationship('Source', backref='url_source_reference')