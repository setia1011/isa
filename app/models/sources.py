from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime, VARCHAR
from sqlalchemy.orm import relationship

class Sources(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True, index=True)
    source = Column(VARCHAR(500), nullable=False, index=True)
    description = Column(VARCHAR(500), index=True)
    site = Column(VARCHAR(50), nullable=False, unique=True, index=True)