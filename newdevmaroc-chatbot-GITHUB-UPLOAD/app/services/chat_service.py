"""
=========================================================
Nom du fichier : chat_service.py
Description : Logique métier pour la gestion des conversations et des réponses.
Objectif : Orchestrer la logique principale de conversation entre l'utilisateur et le bot.
Fonctionnement : Fait le lien entre la réception d'un message, la sauvegarde en base de données, l'appel à l'IA pour générer une réponse, et le renvoi de la réponse.
=========================================================
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.message_repo import MessageRepository
from app.db.repositories.user_repo import UserRepository
from app.ai.llm_client import LLMClient
from app.ai.response_parser import parse_llm_response
from app.services.service_handler import ServiceHandler
from app.config import settings
from app.utils.logger import logger

class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.message_repo = MessageRepository(session)
        self.user_repo = UserRepository(session)
        self.llm_client = LLMClient()
        self.service_handler = ServiceHandler()

    async def get_reply(self, telegram_id: int, user_message: str) -> str:
        """
        Traite le message d'un utilisateur, l'enregistre en DB, 
        appelle l'IA avec le contexte, et sauvegarde la réponse.
        
        Flux intelligent:
        1. Si c'est une question sur les services -> retourne les données réelles du backend
        2. Sinon -> appelle le LLM
        3. Si LLM échoue -> retourne message d'erreur contextuel
        """
        # On suppose que l'utilisateur existe déjà via start ou middleware
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            logger.error(f"Utilisateur {telegram_id} non trouvé pour le chat.")
            return "Une erreur est survenue avec votre profil. Tapez /start s'il vous plaît."

        user_id = user.id

        # 1. Sauvegarder le message de l'utilisateur
        await self.message_repo.add_message(user_id=user_id, role="user", content=user_message)

        # 2. FLUX INTELLIGENT: Détecter si c'est une question sur les services
        # On a désactivé l'interception stricte pour permettre au LLM de "yt7awr" (discuter)
        # service_response = self.service_handler.handle_service_inquiry(user_message)
        # if service_response:
        #     logger.info(f"Service query from {telegram_id}: responding with backend data")
        #     await self.message_repo.add_message(user_id=user_id, role="assistant", content=service_response)
        #     return service_response

        # 3. Récupérer l'historique
        history = await self.message_repo.get_history(user_id=user_id, limit=settings.MAX_HISTORY_MESSAGES)

        # 4. Appeler le LLM RAG LangChain
        raw_response = await self.llm_client.generate_response(history, user_message)

        # 5. Parser la réponse
        final_response = parse_llm_response(raw_response)

        # 7. Sauvegarder la réponse de l'assistant si on en a une valide (pas d'erreur critique)
        if raw_response:
            await self.message_repo.add_message(user_id=user_id, role="assistant", content=final_response)

        return final_response

    async def clear_chat(self, telegram_id: int) -> bool:
        """Efface l'historique de chat de l'utilisateur."""
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False
        await self.message_repo.clear_history(user.id)
        return True
