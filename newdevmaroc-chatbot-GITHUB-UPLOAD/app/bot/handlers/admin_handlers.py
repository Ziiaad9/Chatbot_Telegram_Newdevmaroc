"""
=========================================================
Nom du fichier : admin_handlers.py
Description : Gestion des commandes et actions réservées aux administrateurs.
Objectif : Gérer les commandes spécifiques aux administrateurs du bot (ex: /stats).
Fonctionnement : Intercepte les commandes, vérifie si l'utilisateur est admin, et exécute l'action d'administration demandée.
=========================================================
"""

from telegram import Update
from telegram.ext import ContextTypes
import io
import csv
from app.db.database import AsyncSessionLocal
from app.db.repositories.message_repo import MessageRepository
from app.ai.knowledge_base_loader import KnowledgeBase
from app.services.stats_service import StatsService
from app.services.user_service import UserService
from app.bot.middlewares.auth_middleware import auth_middleware, admin_only

@auth_middleware
@admin_only
async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /admin_stats (Admin uniquement)."""
    async with AsyncSessionLocal() as session:
        stats_service = StatsService(session)
        stats_text = await stats_service.get_global_stats()
        
    await update.message.reply_text(stats_text)

@auth_middleware
@admin_only
async def admin_ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gère la commande /admin_ban <user_id> (Admin uniquement).
    Bannit un utilisateur via son ID Telegram.
    """
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Usage : /admin_ban <telegram_id>")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("L'ID doit être un nombre.")
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        success = await user_service.ban_user(target_id)
        
    if success:
        await update.message.reply_text(f"✅ Utilisateur {target_id} a été banni.")
    else:
        await update.message.reply_text(f"❌ Utilisateur non trouvé ou déjà banni.")

@auth_middleware
@admin_only
async def admin_unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gère la commande /admin_unban <user_id> (Admin uniquement).
    Débannit un utilisateur via son ID Telegram.
    """
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Usage : /admin_unban <telegram_id>")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("L'ID doit être un nombre.")
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        success = await user_service.unban_user(target_id)
        
    if success:
        await update.message.reply_text(f"✅ Utilisateur {target_id} a été débanni.")
    else:
        await update.message.reply_text(f"❌ Utilisateur non trouvé ou pas banni.")

@auth_middleware
@admin_only
async def admin_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gère la commande /broadcast <message> (Admin uniquement).
    Diffuse le message à tous les utilisateurs non bannis.
    """
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Usage : /broadcast <Votre message ici>")
        return

    message = " ".join(context.args)
    
    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        users = await user_service.get_all_users_for_broadcast()
        
    if not users:
        await update.message.reply_text("❌ Aucun utilisateur trouvé pour la diffusion.")
        return

    await update.message.reply_text(f"📢 Diffusion en cours pour {len(users)} utilisateurs...")
    
    success_count = 0
    fail_count = 0
    
    for user in users:
        try:
            await context.bot.send_message(chat_id=user.telegram_id, text=message)
            success_count += 1
        except Exception:
            fail_count += 1
            
    await update.message.reply_text(
        f"✅ Diffusion terminée !\n"
        f"📩 Messages envoyés avec succès : {success_count}\n"
        f"❌ Échecs d'envoi : {fail_count}"
    )

@auth_middleware
@admin_only
async def admin_export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exporte la liste des utilisateurs en CSV."""
    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        users = await user_service.get_all_users()
        
    if not users:
        await update.message.reply_text("Aucun utilisateur à exporter.")
        return
        
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Telegram ID', 'Username', 'First Name', 'Created At', 'Banned'])
    
    for u in users:
        writer.writerow([u.id, u.telegram_id, u.username, u.first_name, u.created_at, u.is_banned])
        
    csv_bytes = output.getvalue().encode('utf-8')
    await update.message.reply_document(
        document=csv_bytes, 
        filename="users_export.csv",
        caption="📊 Voici l'export complet de vos utilisateurs."
    )

@auth_middleware
@admin_only
async def admin_history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Affiche l'historique des conversations d'un utilisateur."""
    if not context.args or len(context.args) == 0:
        await update.message.reply_text("Usage : /admin_history <telegram_id>")
        return

    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("L'ID doit être un nombre.")
        return

    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        target_user = await user_service.get_user(target_id)
        
        if not target_user:
            await update.message.reply_text("❌ Utilisateur introuvable dans la base.")
            return
            
        msg_repo = MessageRepository(session)
        messages = await msg_repo.get_history(user_id=target_user.id, limit=20)
        
    if not messages:
        await update.message.reply_text("L'historique de cet utilisateur est vide.")
        return
        
    text = f"📜 *Historique de {target_user.first_name}* (ID: {target_user.telegram_id})\n\n"
    for msg in messages:
        icon = "🧑‍🦱" if msg.role == "user" else "🤖"
        text += f"{icon} *{msg.role.upper()}* : {msg.content}\n\n"
        
    # Couper si le texte est trop long
    if len(text) > 4000:
        text = text[:4000] + "\n\n... [Coupé car trop long]"
        
    await update.message.reply_text(text, parse_mode="Markdown")

@auth_middleware
@admin_only
async def admin_reload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recharge le fichier de base de connaissances JSON."""
    try:
        kb = KnowledgeBase()
        kb.reload()
        await update.message.reply_text("🔄 Base de connaissances rechargée avec succès !")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur lors du rechargement : {e}")

@auth_middleware
@admin_only
async def admin_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Affiche la liste des commandes administrateur."""
    help_text = (
        "🛠 *Commandes Administrateur* :\n\n"
        "📊 `/admin_stats` - Afficher les statistiques globales\n"
        "⛔️ `/admin_ban <id>` - Bannir un utilisateur\n"
        "🔓 `/admin_unban <id>` - Débannir un utilisateur\n"
        "📢 `/broadcast <message>` - Envoyer un message à tous\n"
        "📥 `/admin_export` - Télécharger les utilisateurs en CSV\n"
        "🔍 `/admin_history <id>` - Voir l'historique d'un user\n"
        "🔄 `/admin_reload` - Recharger le fichier JSON\n"
        "❓ `/admin_help` - Afficher ce menu\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")
