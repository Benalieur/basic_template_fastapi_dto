from pydantic import BaseModel, ConfigDict


class VilleCreate(BaseModel):
    """DTO reçu pour créer ou modifier une ville."""
    nom: str
    latitude: float
    longitude: float


class VilleRead(VilleCreate):
    """DTO renvoyé au client."""
    model_config = ConfigDict(from_attributes=True)  # permet de lire un objet ORM

    id: int


class VilleUpdate(BaseModel):
    """DTO reçu pour une modification partielle (PATCH) : tous les champs sont optionnels."""
    nom: str | None = None
    latitude: float | None = None
    longitude: float | None = None
