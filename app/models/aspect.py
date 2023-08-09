from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class Aspect(Base):
    __tablename__ = 'aspect'
    id = Column(Integer, primary_key=True, index=True)
    aspect = Column(VARCHAR(120), nullable=False, index=True)
    description = Column(VARCHAR(500), index=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False, index=True)

    project = relationship('Project', backref='aspect_project_reference')