from sqlalchemy.orm import Session
from stock.services import create_project
from stock.schemas import ProjectCreate
from db import SessionLocal
from app.db import SessionLocal


# List of projects
projects = [
    {
        "nom": "AAMAL HR BOT",
        "description": (
            "AAMAL HR BOT est un assistant RH intelligent qui automatise les entretiens "
            "d'embauche et l’analyse des CV. Il permet de gagner du temps et de trouver "
            "les meilleurs candidats rapidement."
        ),
        "objectif": "Simplifier le processus de recrutement pour les équipes RH.",
    },
    {
        "nom": "AAMAL STUDENTS",
        "description": (
            "Une plateforme de recrutement dédiée aux étudiants, AAMAL STUDENTS facilite "
            "la mise en relation entre les étudiants et les recruteurs grâce à un système "
            "de matching performant."
        ),
        "objectif": (
            "Aider les étudiants à trouver leur premier emploi ou stage facilement."
        ),
    },
    {
        "nom": "KanonGPT",
        "description": (
            "KanonGPT est un chatbot intelligent spécialisé dans l'assistance et la recherche juridique. "
            "Il fournit des réponses précises aux questions de droit et aide à la compréhension des lois."
        ),
        "objectif": "Rendre le droit accessible à tous avec des réponses rapides et fiables.",
    },
]

# Insert projects into the database
def populate_database():
    db: Session = SessionLocal()
    try:
        for project_data in projects:
            project = ProjectCreate(**project_data)
            create_project(db=db, project=project)
        db.commit()
        print("Database populated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
