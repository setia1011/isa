from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class Sentence(Base):
    __tablename__ = 'sentence'
    id = Column(Integer, primary_key=True, index=True)
    sentence = Column(TEXT)
    content_id = Column(Integer, ForeignKey('content.id'), nullable=False, index=True)
    url_id = Column(Integer, ForeignKey('url.id'), nullable=False, index=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False, index=True)

    content = relationship('Content', backref='sentence_content_reference')
    url = relationship('Url', backref='sentence_url_reference')
    source = relationship('Source', backref='sentence_source_reference')