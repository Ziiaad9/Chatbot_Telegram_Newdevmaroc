"""
=========================================================
Nom du fichier : message_repo.py
Description : Opérations de base de données (CRUD) pour les messages.
Objectif : Gérer toutes les opérations d'accès aux données pour la table des messages (historique de chat).
Fonctionnement : Fournit des fonctions pour ajouter un message, récupérer l'historique d'un utilisateur, ou supprimer des messages.
=========================================================
"""

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Message

class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, user_id: int, role: str, content: str) -> Message:
        """Ajoute un nouveau message dans l'historique."""
        msg = Message(user_id=user_id, role=role, content=content)
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg

    async def get_history(self, user_id: int, limit: int = 10) -> list[Message]:
        """Récupère les derniers messages de l'utilisateur."""
        # On récupère d'abord les plus récents, puis on inverse la liste
        stmt = select(Message).where(Message.user_id == user_id).order_by(Message.id.desc()).limit(limit)
        result = await self.session.execute(stmt)
        messages = result.scalars().all()
        return list(reversed(messages))

    async def clear_history(self, user_id: int) -> None:
        """Supprime tout l'historique d'un utilisateur."""
        stmt = delete(Message).where(Message.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def count_by_user(self, user_id: int) -> int:
        """Compte le nombre total de messages envoyés par/pour un utilisateur."""
        stmt = select(func.count(Message.id)).where(Message.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def count_total(self) -> int:
        """Compte le nombre total de messages enregistrés dans tout le système."""
        stmt = select(func.count(Message.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0
