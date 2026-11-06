from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.database import Base, engine
from app.models import ville  # noqa: F401  (enregistre le modèle avant create_all)

# Crée les tables au démarrage (pour une démo ; en prod on utiliserait Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Villes")
app.include_router(api_router, prefix="/api/v1")
