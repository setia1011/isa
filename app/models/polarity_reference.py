from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

class PolarityReference(Base):
    __tablename__ = 'polarity_reference'
    id = Column(Integer, primary_key=True, index=True)
    polarity = Column(VARCHAR(120), nullable=False, index=True)
    description = Column(VARCHAR(500), index=True)