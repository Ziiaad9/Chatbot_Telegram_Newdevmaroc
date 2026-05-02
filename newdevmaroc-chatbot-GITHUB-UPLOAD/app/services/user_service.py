"""
=========================================================
Nom du fichier : user_service.py
Description : Logique métier liée à la gestion des utilisateurs.
Objectif : Gérer la logique métier liée au cycle de vie d'un utilisateur.
Fonctionnement : S'assure que chaque nouvel utilisateur est bien enregistré, met à jour ses informations et gère son statut.
=========================================================
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.user_repo import UserRepository
from app.db.models import User

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def ensure_user_exists(self, telegram_id: int, username: str = None, first_name: str = None) -> User:
        """S'assure que l'utilisateur existe dans la base de données."""
        return await self.user_repo.get_or_create(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name
        )

    async def get_user(self, telegram_id: int) -> User | None:
        """Récupère un utilisateur via son ID Telegram."""
        return await self.user_repo.get_by_telegram_id(telegram_id)

    async def ban_user(self, telegram_id: int) -> bool:
        """Bannit un utilisateur."""
        return await self.user_repo.ban_user(telegram_id)

    async def unban_user(self, telegram_id: int) -> bool:
        """Débannit un utilisateur."""
        return await self.user_repo.unban_user(telegram_id)

    async def get_all_users(self) -> list[User]:
        """Récupère tous les utilisateurs pour l'export."""
        return await self.user_repo.get_all_users()

    async def get_all_users_for_broadcast(self) -> list[User]:
        """Récupère tous les utilisateurs pour la diffusion (broadcasting)."""
        return await self.user_repo.get_all_active_users()
