"""
=========================================================
Nom du fichier : test_llm_client.py
Description : Tests automatisés pour le client LLM.
Objectif : Vérifier que le client d'IA (llm_client) fonctionne sans erreur.
Fonctionnement : Simule des appels au LLM et vérifie que la réponse retournée a le bon format et contient les informations attendues.
=========================================================
"""

import pytest
from unittest.mock import AsyncMock, patch
from app.ai.llm_client import LLMClient
from app.ai.prompt_builder import build_messages_payload
from app.db.models import Message

@pytest.mark.asyncio
async def test_llm_client_generate_response():
    """Test le client LLM avec un mock de l'API Groq."""
    client = LLMClient()
    
    with patch.object(client.client.chat.completions, 'create', new_callable=AsyncMock) as mock_create:
        mock_create.return_value.choices = [
            type('obj', (object,), {'message': type('obj', (object,), {'content': 'Hello from AI'})()})
        ]
        
        response = await client.generate_response([{"role": "user", "content": "Hi"}])
        assert response == "Hello from AI"
        mock_create.assert_called_once()

def test_prompt_builder():
    """Test la construction du prompt."""
    msgs = [Message(role="user", content="Hello")]
    payload = build_messages_payload(msgs)
    
    assert len(payload) == 2
    assert payload[0]["role"] == "system"
    assert payload[1]["role"] == "user"
    assert payload[1]["content"] == "Hello"
