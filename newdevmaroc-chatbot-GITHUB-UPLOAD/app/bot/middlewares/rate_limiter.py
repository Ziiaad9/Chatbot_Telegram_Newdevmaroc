"""
=========================================================
Nom du fichier : rate_limiter.py
Description : Middleware pour limiter le nombre de requêtes (anti-spam).
Objectif : Empêcher les abus (spam) en limitant le nombre de messages qu'un utilisateur peut envoyer en peu de temps.
Fonctionnement : Compte le nombre de requêtes par utilisateur dans un laps de temps défini et bloque temporairement si la limite est dépassée.
=========================================================
"""

import time
import asyncio
from typing import Dict, List
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from app.config import settings

# Structure: { user_id: [timestamp1, timestamp2, ...] }
_RATE_LIMIT_STORE: Dict[int, List[float]] = {}
_MAX = settings.RATE_LIMIT_MAX
_WINDOW = settings.RATE_LIMIT_WINDOW

class RateLimitExceeded(Exception):
    pass

def _cleanup_old_entries(user_id: int, current_time: float):
    """Enlève les timestamps plus vieux que THE_WINDOW."""
    if user_id in _RATE_LIMIT_STORE:
        _RATE_LIMIT_STORE[user_id] = [
            ts for ts in _RATE_LIMIT_STORE[user_id]
            if current_time - ts < _WINDOW
        ]

def rate_limit_decorator(func):
    """Décorateur pour limiter les requêtes des utilisateurs."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_user:
            return await func(update, context, *args, **kwargs)

        user_id = update.effective_user.id
        current_time = time.time()

        _cleanup_old_entries(user_id, current_time)

        # Si l'utilisateur n'est pas dans le store, on initialise
        if user_id not in _RATE_LIMIT_STORE:
            _RATE_LIMIT_STORE[user_id] = []

        if len(_RATE_LIMIT_STORE[user_id]) >= _MAX:
            remaining_time = _WINDOW - (current_time - _RATE_LIMIT_STORE[user_id][0])
            minutes = int(remaining_time // 60) or 1
            await update.message.reply_text(
                f"⚠️ Oups ! Vous avez envoyé trop de messages. Veuillez patienter {minutes} minute(s)."
            )
            return  # Stop execution

        # Ajouter la requête
        _RATE_LIMIT_STORE[user_id].append(current_time)

        return await func(update, context, *args, **kwargs)
    return wrapper
