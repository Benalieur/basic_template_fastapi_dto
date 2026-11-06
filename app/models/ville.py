from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Ville(Base):
    __tablename__ = "villes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
