"""
=========================================================
Nom du fichier : application.py
Description : Initialisation et configuration de l'application du bot Telegram.
Objectif : Configurer et instancier le bot Telegram de façon asynchrone.
Fonctionnement : Associe le token du bot, ajoute les handlers (gestionnaires de messages/commandes) et les middlewares.
=========================================================
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from app.config import settings
from app.bot.handlers.command_handlers import start_command, help_command, reset_command, stats_command, services_command, contact_command
from app.bot.handlers.message_handlers import handle_message
from app.bot.handlers.admin_handlers import (
    admin_ban_command, admin_stats_command, admin_broadcast_command,
    admin_unban_command, admin_export_command, admin_history_command,
    admin_reload_command, admin_help_command
)

def build_application():
    """Construit et configure l'application Telegram Bot."""
    # Création de l'application
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Ajout des handlers de commandes basiques
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("stats", stats_command))
    
    # Ajout des handlers administrateur
    app.add_handler(CommandHandler("admin_ban", admin_ban_command))
    app.add_handler(CommandHandler("admin_unban", admin_unban_command))
    app.add_handler(CommandHandler("admin_stats", admin_stats_command))
    app.add_handler(CommandHandler("broadcast", admin_broadcast_command))
    app.add_handler(CommandHandler("admin_export", admin_export_command))
    app.add_handler(CommandHandler("admin_history", admin_history_command))
    app.add_handler(CommandHandler("admin_reload", admin_reload_command))
    app.add_handler(CommandHandler("admin_help", admin_help_command))
    
    # Ajout du handler pour tous les messages texte
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return app
