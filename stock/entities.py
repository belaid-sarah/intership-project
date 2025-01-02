# stock/entities.py
from sqlalchemy import Column, Integer, String
from .db import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(String)
    objectif = Column(String)
