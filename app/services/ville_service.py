from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.ville import VilleCreate, VilleUpdate
from app.models.ville import Ville
from app.repositories import ville_repository


def lister(db: Session) -> list[Ville]:
    return ville_repository.get_all(db)


def recuperer(db: Session, ville_id: int) -> Ville:
    ville = ville_repository.get_by_id(db, ville_id)
    if ville is None:
        raise HTTPException(status_code=404, detail="Ville introuvable")
    return ville


def creer(db: Session, data: VilleCreate) -> Ville:
    ville = Ville(**data.model_dump())  # DTO -> modèle ORM
    return ville_repository.save(db, ville)


def modifier(db: Session, ville_id: int, data: VilleCreate) -> Ville:
    ville = recuperer(db, ville_id)
    ville.nom = data.nom
    ville.latitude = data.latitude
    ville.longitude = data.longitude
    return ville_repository.save(db, ville)


def modifier_partiellement(db: Session, ville_id: int, data: VilleUpdate) -> Ville:
    ville = recuperer(db, ville_id)
    # exclude_unset=True : on ne garde que les champs réellement envoyés par le client
    for champ, valeur in data.model_dump(exclude_unset=True).items():
        setattr(ville, champ, valeur)
    return ville_repository.save(db, ville)


def supprimer(db: Session, ville_id: int) -> None:
    ville = recuperer(db, ville_id)
    ville_repository.delete(db, ville)
