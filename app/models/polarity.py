from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class Polarity(Base):
    __tablename__ = 'polarity'
    id = Column(Integer, primary_key=True, index=True)
    sentence_id = Column(Integer, ForeignKey('sentence.id'), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False, index=True)
    polarity_reference_id = Column(Integer, ForeignKey('polarity_reference.id'), nullable=False, index=True)
    aspect_id = Column(Integer, ForeignKey('aspect.id'), nullable=False, index=True)
    reviewer_id = Column(Integer, nullable=False, index=True)

    sentence = relationship('Sentence', backref='polarity_sentence_reference')
    project = relationship('Project', backref='polarity_project_reference')
    polarity_reference = relationship('PolarityReference', backref='polarity_polarity_reference')
    aspect = relationship('Aspect', backref='polarity_aspect_reference')