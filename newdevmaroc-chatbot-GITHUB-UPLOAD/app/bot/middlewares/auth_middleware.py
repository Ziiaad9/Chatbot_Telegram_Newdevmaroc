"""
=========================================================
Nom du fichier : auth_middleware.py
Description : Middleware pour l'authentification et l'autorisation des utilisateurs.
Objectif : Vérifier l'identité et les droits des utilisateurs avant de traiter leurs messages.
Fonctionnement : Intercepte la requête entrante, vérifie dans la base de données si l'utilisateur est connu/banni, et autorise ou bloque l'accès.
=========================================================
"""

from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from app.db.database import AsyncSessionLocal
from app.db.repositories.user_repo import UserRepository
from app.config import settings

def auth_middleware(func):
    """
    Décorateur pour vérifier si l'utilisateur est banni avant de traiter son message.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.effective_user:
            return await func(update, context, *args, **kwargs)

        user_id = update.effective_user.id
        
        async with AsyncSessionLocal() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_telegram_id(user_id)
            
            if user and user.is_banned:
                await update.message.reply_text(
                    "❌ Vous avez été banni de l'utilisation de ce bot. "
                    "Veuillez contacter le support."
                )
                return # Stop execution
            
        return await func(update, context, *args, **kwargs)
    return wrapper

def admin_only(func):
    """
    Décorateur pour réserver l'accès aux administrateurs.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_user.id not in settings.admin_ids_list:
            await update.message.reply_text("⛔️ Commande réservée aux administrateurs.")
            return # Stop execution
            
        return await func(update, context, *args, **kwargs)
    return wrapper
