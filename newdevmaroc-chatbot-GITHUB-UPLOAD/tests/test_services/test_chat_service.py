"""
=========================================================
Nom du fichier : test_chat_service.py
Description : Tests automatisés pour le service de chat.
Objectif : Vérifier que le service de chat coordonne bien la BD, l'IA et l'utilisateur.
Fonctionnement : Simule le flux complet d'une conversation et vérifie que l'historique est sauvegardé et que la réponse est bien générée.
=========================================================
"""

import pytest
from app.services.chat_service import ChatService
from app.services.user_service import UserService
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_chat_service_get_reply(db_session):
    """Test le flux complet de chat_service avec un utilisateur fictif."""
    user_service = UserService(db_session)
    user = await user_service.ensure_user_exists(telegram_id=456)
    
    chat_service = ChatService(db_session)
    
    with patch.object(chat_service.llm_client, 'generate_response', new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Salut, je suis une IA de test."
        
        reply = await chat_service.get_reply(456, "Bonjour")
        assert reply == "Salut, je suis une IA de test."
        
        # Vérifions que le message a été ajouté
        history = await chat_service.message_repo.get_history(user.id)
        assert len(history) == 2 # 1 User, 1 Assistant
        assert history[0].role == "user"
        assert history[1].role == "assistant"
