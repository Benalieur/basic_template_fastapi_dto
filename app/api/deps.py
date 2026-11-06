from app.core.database import SessionLocal


def get_db():
    """Ouvre une session BDD par requête et la ferme à la fin."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
