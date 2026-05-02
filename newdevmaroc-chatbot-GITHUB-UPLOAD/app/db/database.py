"""
=========================================================
Nom du fichier : database.py
Description : Configuration et connexion à la base de données (SQLite/SQLAlchemy).
Objectif : Configurer la connexion à la base de données asynchrone.
Fonctionnement : Crée le moteur de base de données (engine), définit la session (sessionmaker) et la classe de base pour les modèles (Base).
=========================================================
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Engine SQLAlchemy asynchrone pointant vers le SQLite
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Session asynchrone
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    """Classe de base pour tous les modèles SQLAlchemy"""
    pass

async def get_db_session():
    """Générateur de session DB pour l'utilisation dans le code."""
    async with AsyncSessionLocal() as session:
        yield session
