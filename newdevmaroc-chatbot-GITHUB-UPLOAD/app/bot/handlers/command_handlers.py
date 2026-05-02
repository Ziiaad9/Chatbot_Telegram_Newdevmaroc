"""
=========================================================
Nom du fichier : command_handlers.py
Description : Gestion des commandes de base du bot (ex: /start, /help).
Objectif : Gérer les commandes de base envoyées par tous les utilisateurs.
Fonctionnement : Définit les fonctions qui sont appelées lorsque l'utilisateur tape une commande spécifique et renvoie la réponse appropriée.
=========================================================
"""

from telegram import Update
from telegram.ext import ContextTypes
from app.db.database import AsyncSessionLocal
from app.services.user_service import UserService
from app.services.chat_service import ChatService
from app.services.stats_service import StatsService
from app.services.service_handler import ServiceHandler
from app.bot.middlewares.auth_middleware import auth_middleware
from app.bot.middlewares.rate_limiter import rate_limit_decorator

@rate_limit_decorator
@auth_middleware
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /start."""
    user = update.effective_user
    
    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        # S'assure que l'utilisateur est en DB
        await user_service.ensure_user_exists(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name
        )
        
    # Send Welcome Banner
    try:
        from pathlib import Path
        logo_path = Path(__file__).resolve().parent.parent.parent.parent / "NewDevMaroc Logo.png"
        if logo_path.exists():
            with open(logo_path, "rb") as photo:
                await update.message.reply_photo(photo=photo)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error sending logo: {e}")

    await update.message.reply_text(
        f"👋 Bonjour {user.first_name or '!'}\n\n"
        "Je suis l'assistant virtuel de **NewDevMaroc** 🇲🇦.\n"
        "Comment puis-je vous aider aujourd'hui concernant nos services web et digitaux ?\n\n"
        "Tapez /help pour voir mes commandes disponibles."
    )

@rate_limit_decorator
@auth_middleware
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /help."""
    help_text = (
        "🛠 **Commandes disponibles :**\n\n"
        "/start - Démarrer le bot\n"
        "/help - Afficher ce message d'aide\n"
        "/services - Voir la liste complète de nos services\n"
        "/contact - Nous contacter directement\n"
        "/reset - Effacer l'historique de notre conversation\n"
        "/stats - Voir vos statistiques personnelles\n\n"
        "Vous pouvez simplement m'écrire pour discuter de vos projets !"
    )
    await update.message.reply_text(help_text)

@rate_limit_decorator
@auth_middleware
async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /services."""
    service_handler = ServiceHandler()
    response = service_handler.get_services_response("")
    await update.message.reply_text(response)

@rate_limit_decorator
@auth_middleware
async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /contact."""
    contact_text = (
        "📧 **Contactez-nous directement :**\n\n"
        "Email: contact@newdevmaroc.com\n"
        "Téléphone: Écrivez-nous pour plus de détails\n\n"
        "Ou tapez votre message et demande ci-dessous, nous vous répondrons rapidement! 😊"
    )
    await update.message.reply_text(contact_text)

@rate_limit_decorator
@auth_middleware
async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /reset."""
    user_id = update.effective_user.id
    
    async with AsyncSessionLocal() as session:
        chat_service = ChatService(session)
        success = await chat_service.clear_chat(user_id)
        
    if success:
        await update.message.reply_text("🧹 Votre historique a été effacé avec succès.")
    else:
        await update.message.reply_text("❌ Une erreur est survenue lors de l'effacement.")

@rate_limit_decorator
@auth_middleware
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /stats."""
    user_id = update.effective_user.id
    
    async with AsyncSessionLocal() as session:
        stats_service = StatsService(session)
        stats_text = await stats_service.get_personal_stats(user_id)
        
    await update.message.reply_text(stats_text)
