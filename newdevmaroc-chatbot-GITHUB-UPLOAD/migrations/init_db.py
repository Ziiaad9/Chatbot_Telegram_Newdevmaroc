"""
=========================================================
Nom du fichier : init_db.py
Description : Script pour initialiser la base de données et créer les tables.
Objectif : Créer physiquement les tables dans la base de données.
Fonctionnement : Importe les modèles et utilise SQLAlchemy pour créer le schéma de la base de données si elle n'existe pas encore.
=========================================================
"""

import asyncio
import os
import sys

# Ajouter le répertoire racine au PYTHONPATH pour permettre les imports absolus
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine, Base
from app.utils.logger import logger

async def init_models():
    """Crée les tables dans la base de données SQLite."""
    # Assurer que le dossier data existe
    os.makedirs("./data", exist_ok=True)
    
    async with engine.begin() as conn:
        logger.info("Suppression des anciennes tables...")
        await conn.run_sync(Base.metadata.drop_all)
        
        logger.info("Création des nouvelles tables...")
        await conn.run_sync(Base.metadata.create_all)
        
    logger.info("Base de données initialisée avec succès.")

if __name__ == "__main__":
    asyncio.run(init_models())
