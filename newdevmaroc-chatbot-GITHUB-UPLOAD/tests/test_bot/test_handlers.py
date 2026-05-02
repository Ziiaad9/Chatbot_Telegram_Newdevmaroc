"""
=========================================================
Nom du fichier : test_handlers.py
Description : Tests automatisés pour les gestionnaires (handlers) du bot.
Objectif : Vérifier que les gestionnaires de messages du bot réagissent correctement.
Fonctionnement : Envoie de faux messages au bot dans un environnement de test et vérifie les réponses générées par les handlers.
=========================================================
"""

import pytest
from telegram import Update, Message, Chat, User
from unittest.mock import AsyncMock, patch
from app.bot.handlers.command_handlers import start_command

@pytest.mark.asyncio
async def test_start_command():
    """Test basique de la commande /start."""
    # Mocks
    user = User(id=123, first_name="Test", is_bot=False)
    chat = Chat(id=123, type="private")
    message = Message(message_id=1, date=None, chat=chat, text="/start", from_user=user)
    
    update = Update(update_id=1, message=message)
    context = AsyncMock()
    
    # Mock de reply_text
    update.message.reply_text = AsyncMock()
    
    with patch('app.bot.handlers.command_handlers.UserService') as MockUserService:
        mock_service = MockUserService.return_value
        mock_service.ensure_user_exists = AsyncMock()
        
        with patch('app.bot.handlers.command_handlers.AsyncSessionLocal') as MockSession:
            # Execution
            await start_command(update, context)
            
            # Verifications
            MockUserService.assert_called_once()
            mock_service.ensure_user_exists.assert_called_once_with(telegram_id=123, username=None, first_name="Test")
            update.message.reply_text.assert_called_once()
