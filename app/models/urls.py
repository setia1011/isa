from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Enum, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class Urls(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, index=True)
    crawled_at = Column(TIMESTAMP, nullable=False, index=True)
    url = Column(VARCHAR(500), unique=True, index=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False, index=True)
    status = Column(Enum('Y','N'), nullable=False, index=True)
    
    ref_source = relationship('Sources', backref='urls')