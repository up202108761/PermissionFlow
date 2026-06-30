from app.database import SessionLocal
from app.models import User, Application

db = SessionLocal()

# Evitar inserir dados duplicados
if db.query(User).count() == 0:

    alexandra = User(
        name="Alexandra Torres",
        email="alexandra@permissionflow.pt",
        role="owner"
    )

    goncalo = User(
        name="Gonçalo Matos",
        email="goncalo@permissionflow.pt",
        role="employee"
    )

    joao = User(
        name="João Chaves",
        email="joao@permissionflow.pt",
        role="employee"
    )

    db.add_all([alexandra, goncalo, joao])
    db.commit()

    db.refresh(alexandra)

    applications = [
        Application(
            name="Jira",
            description="Project Management",
            owner_id=alexandra.id
        ),
        Application(
            name="GitHub Enterprise",
            description="Source Code Management",
            owner_id=alexandra.id
        ),
        Application(
            name="SAP",
            description="Enterprise Resource Planning",
            owner_id=alexandra.id
        )
    ]

    db.add_all(applications)
    db.commit()

print("Database seeded successfully!")

db.close()