from pydantic import BaseModel

class ProjectBase(BaseModel):
    nom: str
    description: str = None
    objectif: str = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True
