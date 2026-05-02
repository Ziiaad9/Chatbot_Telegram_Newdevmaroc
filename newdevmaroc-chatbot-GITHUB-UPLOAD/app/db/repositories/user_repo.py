"""
=========================================================
Nom du fichier : user_repo.py
Description : Opérations de base de données (CRUD) pour les utilisateurs.
Objectif : Gérer toutes les opérations d'accès aux données pour la table des utilisateurs.
Fonctionnement : Fournit des fonctions pour créer un utilisateur, le rechercher par son ID Telegram, le mettre à jour ou le bannir.
=========================================================
"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Récupère un utilisateur par son identifiant Telegram."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, telegram_id: int, username: str = None, first_name: str = None) -> User:
        """Crée un nouvel utilisateur."""
        user = User(telegram_id=telegram_id, username=username, first_name=first_name)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
        
    async def get_or_create(self, telegram_id: int, username: str = None, first_name: str = None) -> User:
        """Récupère l'utilisateur ou le crée s'il n'existe pas."""
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.create(telegram_id, username, first_name)
        return user

    async def ban_user(self, telegram_id: int) -> bool:
        """Bannit un utilisateur. Retourne True si action effectuée."""
        user = await self.get_by_telegram_id(telegram_id)
        if user and not user.is_banned:
            user.is_banned = True
            await self.session.commit()
            return True
        return False

    async def unban_user(self, telegram_id: int) -> bool:
        """Débannit un utilisateur. Retourne True si action effectuée."""
        user = await self.get_by_telegram_id(telegram_id)
        if user and user.is_banned:
            user.is_banned = False
            await self.session.commit()
            return True
        return False

    async def get_all_users(self) -> list[User]:
        """Récupère tous les utilisateurs enregistrés."""
        stmt = select(User)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_total(self) -> int:
        """Compte le nombre total d'utilisateurs inscrits."""
        stmt = select(func.count(User.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def get_all_active_users(self) -> list[User]:
        """Récupère tous les utilisateurs non bannis."""
        stmt = select(User).where(User.is_banned == False)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
