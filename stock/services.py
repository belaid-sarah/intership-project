from sqlalchemy.orm import Session
from .entities import Project
from stock.schemas import ProjectCreate, ProjectUpdate



# Create a project
def create_project(db: Session, project: ProjectCreate):
    db_project = Project(nom=project.nom, description=project.description, objectif=project.objectif)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# Update a project
def update_project(db: Session, project_id: int, project: ProjectUpdate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db_project.nom = project.nom
        db_project.description = project.description
        db_project.objectif = project.objectif
        db.commit()
        db.refresh(db_project)
        return db_project
    return None

# Delete a project
def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        return db_project
    return None

# Get all projects
def get_projects(db: Session):
    return db.query(Project).all()
