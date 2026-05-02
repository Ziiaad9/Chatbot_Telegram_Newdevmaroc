"""
=========================================================
Nom du fichier : stats_service.py
Description : Logique pour la génération et la gestion des statistiques d'utilisation.
Objectif : Calculer et fournir des statistiques sur l'utilisation du bot.
Fonctionnement : Interroge la base de données pour compter le nombre d'utilisateurs, le volume de messages, etc., utile pour les administrateurs.
=========================================================
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repo import UserRepository
from app.db.repositories.message_repo import MessageRepository
from datetime import datetime

class StatsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.message_repo = MessageRepository(session)

    async def get_personal_stats(self, telegram_id: int) -> str:
        """Récupère les statistiques d'un utilisateur spécifique."""
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return "Vous n'êtes pas encore enregistré."
        
        msg_count = await self.message_repo.count_by_user(user.id)
        date_str = user.created_at.strftime('%d/%m/%Y')
        
        return (
            f"📊 **Statistiques Personnelles :**\n\n"
            f"👤 Inscription : {date_str}\n"
            f"💬 Messages échangés : {msg_count}"
        )

    async def get_global_stats(self) -> str:
        """Récupère les statistiques globales du bot (Admin)."""
        users_count = await self.user_repo.count_total()
        msgs_count = await self.message_repo.count_total()

        return (
            f"👑 **Statistiques Administrateur :**\n\n"
            f"👥 Total utilisateurs : {users_count}\n"
            f"📬 Total messages en base : {msgs_count}"
        )
