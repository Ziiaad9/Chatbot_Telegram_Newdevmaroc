"""
=========================================================
Nom du fichier : logger.py
Description : Configuration de la journalisation (logs) de l'application.
Objectif : Configurer le système d'enregistrement des événements (logs).
Fonctionnement : Définit le format des logs, le niveau de sévérité (INFO, DEBUG, ERROR) et la destination pour faciliter le débogage.
=========================================================
"""

import logging
import sys
from app.config import settings

def setup_logger():
    """
    Configure et retourne le logger de l'application.
    Log à la fois dans la console et dans le fichier chatbot.log
    """
    logger = logging.getLogger("newdevmaroc_bot")
    
    if not logger.handlers:
        level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
        logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # Optionnel: File handler
        try:
            fh = logging.FileHandler("chatbot.log", encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception:
            pass # Si permission refusée, on a au moins la console

    return logger

logger = setup_logger()
