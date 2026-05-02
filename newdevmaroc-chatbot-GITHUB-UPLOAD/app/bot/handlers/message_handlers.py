"""
=========================================================
Nom du fichier : message_handlers.py
Description : Gestion des messages textuels envoyés par les utilisateurs.
Objectif : Traiter les messages textuels normaux (non-commandes) envoyés par les utilisateurs.
Fonctionnement : Reçoit le texte, le passe au service de chat (qui interroge l'IA) et renvoie la réponse générée à l'utilisateur.
=========================================================
"""

from telegram import Update
from telegram.ext import ContextTypes
from app.db.database import AsyncSessionLocal
from app.services.chat_service import ChatService
from app.bot.middlewares.auth_middleware import auth_middleware
from app.bot.middlewares.rate_limiter import rate_limit_decorator
from app.utils.logger import logger

@rate_limit_decorator
@auth_middleware
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages texte normaux envoyés au bot."""
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    user_id = update.effective_user.id

    # Indiquer que le bot est en train d'écrire
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    try:
        async with AsyncSessionLocal() as session:
            chat_service = ChatService(session)
            reply_text = await chat_service.get_reply(
                telegram_id=user_id,
                user_message=user_text
            )
            
        await update.message.reply_text(reply_text)
    except Exception as e:
        logger.error(f"Erreur lors du traitement du message de {user_id}: {e}", exc_info=True)
        await update.message.reply_text("⚠️ Désolé, une erreur interne est survenue.")
