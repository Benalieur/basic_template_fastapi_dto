from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.schemas.ville import VilleCreate, VilleRead, VilleUpdate
from app.services import ville_service

router = APIRouter(prefix="/villes", tags=["villes"])


@router.get("/", response_model=list[VilleRead])
def lister_villes(db: Session = Depends(get_db)):
    return ville_service.lister(db)


@router.get("/{ville_id}", response_model=VilleRead)
def recuperer_ville(ville_id: int, db: Session = Depends(get_db)):
    return ville_service.recuperer(db, ville_id)


@router.post("/", response_model=VilleRead, status_code=201)
def creer_ville(data: VilleCreate, db: Session = Depends(get_db)):
    return ville_service.creer(db, data)


@router.put("/{ville_id}", response_model=VilleRead)
def modifier_ville(ville_id: int, data: VilleCreate, db: Session = Depends(get_db)):
    return ville_service.modifier(db, ville_id, data)


@router.patch("/{ville_id}", response_model=VilleRead)
def modifier_partiellement_ville(ville_id: int, data: VilleUpdate, db: Session = Depends(get_db)):
    return ville_service.modifier_partiellement(db, ville_id, data)


@router.delete("/{ville_id}", status_code=204)
def supprimer_ville(ville_id: int, db: Session = Depends(get_db)):
    ville_service.supprimer(db, ville_id)
