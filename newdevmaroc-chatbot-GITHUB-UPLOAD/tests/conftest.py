"""
=========================================================
Nom du fichier : conftest.py
Description : Configuration partagée pour les tests automatisés avec pytest.
Objectif : Préparer l'environnement et les fixtures pour les tests automatisés.
Fonctionnement : Définit des objets mockés (fausse base de données, faux clients API) qui seront utilisés par pytest pour les tests.
=========================================================
"""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.database import Base

# Base de données en mémoire pour les tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DATABASE_URL, echo=False)

@pytest.fixture
async def db_session(engine):
    """Fixture qui fournit une session DB vide avec les tables créées pour chaque test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with Session() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
