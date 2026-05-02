"""
=========================================================
Nom du fichier : llm_client.py
Description : Client pour communiquer avec le modèle d'intelligence artificielle (LLM).
Objectif : Gérer la communication directe avec le modèle d'intelligence artificielle (Groq/OpenRouter).
Fonctionnement : Reçoit des prompts, configure les appels API et retourne la réponse générée par l'IA.
=========================================================
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage
from app.config import settings
from app.utils.logger import logger
from app.ai.vector_store import VectorStoreManager

class LLMClient:
    def __init__(self):
        # Utiliser ChatOpenAI configuré pour pointer vers l'API de Groq
        self.llm = ChatOpenAI(
            api_key=settings.GROQ_API_KEY if hasattr(settings, 'GROQ_API_KEY') else "dummy",
            base_url="https://api.groq.com/openai/v1",
            model=settings.OPENROUTER_MODEL, # Ex: llama-3.3-70b-versatile
            temperature=0.7,
            max_tokens=1024
        )
        self.vector_manager = VectorStoreManager()
        self.retriever = self.vector_manager.get_retriever()
        
        # Le prompt RAG
        self.system_prompt = (
            "Tu es l'assistant virtuel de NewDevMaroc. "
            "Utilise EXCLUSIVEMENT les éléments de contexte suivants pour répondre à la question de l'utilisateur.\n"
            "Si la réponse n'est pas dans le contexte, dis poliment que tu ne sais pas et propose de contacter l'équipe.\n"
            "Discute naturellement, sois professionnel et chaleureux.\n\n"
            "Contexte:\n{context}\n\n"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        self.document_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.retrieval_chain = create_retrieval_chain(self.retriever, self.document_chain)
        
        logger.info(f"LLM Client (RAG LangChain) initialized with model: {settings.OPENROUTER_MODEL}")

    async def generate_response(self, history: list, user_message: str) -> str | None:
        """
        Envoie la question à la chaîne RAG LangChain et retourne la réponse.
        """
        try:
            logger.debug(f"Calling RAG Chain...")
            
            # Formater l'historique pour LangChain
            chat_history = []
            for msg in history:
                if msg.role == "user":
                    chat_history.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    chat_history.append(AIMessage(content=msg.content))
            
            # Invoquer la chaîne
            response = await self.retrieval_chain.ainvoke({
                "input": user_message,
                "chat_history": chat_history
            })
            
            return response["answer"]
        except Exception as e:
            logger.error(f"Erreur RAG LangChain (Groq): {str(e)}", exc_info=True)
            return None
