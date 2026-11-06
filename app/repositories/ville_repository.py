from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ville import Ville


def get_all(db: Session) -> list[Ville]:
    return list(db.scalars(select(Ville)))


def get_by_id(db: Session, ville_id: int) -> Ville | None:
    return db.get(Ville, ville_id)


def save(db: Session, ville: Ville) -> Ville:
    db.add(ville)
    db.commit()
    db.refresh(ville)
    return ville


def delete(db: Session, ville: Ville) -> None:
    db.delete(ville)
    db.commit()
