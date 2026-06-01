"""
=========================================================
Nom du fichier : main.py
Description : Point d'entrée principal pour démarrer le bot Telegram.
Objectif : Démarrer l'application et lancer le bot Telegram.
Fonctionnement : Configure le logging, initialise la base de données, construit l'application Telegram et commence à écouter les messages.
=========================================================
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import logging
from app.bot.application import build_application
from app.utils.logger import logger
from app.db.database import engine, Base

async def init_db():
    """Initialise de force la base de données (modèles SQLAlchemy)."""
    async with engine.begin() as conn:
        # En production, utilisez Alembic. Pour la simplicité ici on create_all.
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Base de données initialisée correctement.")
        
    # Initialiser la base vectorielle ChromaDB si nécessaire
    from app.ai.vector_store import VectorStoreManager
    try:
        manager = VectorStoreManager()
        # Appel de get_retriever() qui déclenche l'auto-initialisation si vide/inexistante
        manager.get_retriever()
        logger.info("Base vectorielle verifiee et prete.")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base vectorielle : {e}")

def main():
    """Point d'entrée principal de l'application."""
    logger.info("Démarrage du chatbot NewDevMaroc...")
    
    # On initialise la db avant de lancer le bot
    asyncio.get_event_loop().run_until_complete(init_db())
    
    # Récupération et lancement du bot
    app = build_application()
    
    # Démarre le polling Telegram
    logger.info("Bot en écoute (Polling)...")
    app.run_polling()

if __name__ == "__main__":
    main()
