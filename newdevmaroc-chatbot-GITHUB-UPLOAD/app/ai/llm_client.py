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
            temperature=0.2,
            max_tokens=1024
        )
        self.vector_manager = VectorStoreManager()
        self.retriever = self.vector_manager.get_retriever()
        
        self.system_prompt = (
            "Tu es l'assistant virtuel de l'agence web et digitale NewDevMaroc.\n\n"
            "🎯 RÈGLES DE COMPRÉHENSION ET DE RÉPONSE :\n"
            "1. SOIS PRÉCIS : Réponds EXACTEMENT à ce que l'utilisateur demande. S'il demande UNIQUEMENT la durée (le temps/w9t), ne lui donne pas les prix (taman) sauf s'il le demande.\n"
            "2. VÉRIFICATION STRICTE DU SERVICE : Vérifie toujours si le service demandé existe vraiment dans la description des services du contexte. Si le domaine demandé n'est pas listé (ex: Vente de matériel, Hacking, Médecine, Smartphones), tu DOIS lui dire poliment (DANS SA LANGUE) que l'agence ne fait pas ce type de service. NE RIEN INVENTER.\n"
            "3. NE RIEN INVENTER : Base-toi uniquement sur le contexte.\n"
            "4. MISE EN FORME : Aère tes réponses et utilise des emojis.\n\n"
            "📚 CONTEXTE DE RECHERCHE :\n{context}\n\n"
            "🚨 RÈGLES DE LANGUE ET EFFET MIROIR (TRÈS IMPORTANT) :\n"
            "1. EFFET MIROIR STRICT : Tu dois IMPÉRATIVEMENT répondre dans la MÊME LANGUE que le TOUT DERNIER MESSAGE de l'utilisateur.\n"
            "   ⚠️ ATTENTION : Ne te laisse PAS influencer par la langue de l'historique ! Même si les 10 derniers messages étaient en Français, si la NOUVELLE question est en Anglais, tu DOIS répondre en Anglais.\n"
            "   - Si le DERNIER message est en Anglais = Réponse en ANGLAIS.\n"
            "   - Si le DERNIER message est en Français = Réponse 100% en FRANÇAIS (Aucun mot en darija).\n"
            "   - Si le DERNIER message est en Arabe classique = Réponse en ARABE CLASSIQUE.\n"
            "   - Si le DERNIER message est en Darija (ex: bch7al, kifach) = Réponse 100% en DARIJA MAROCAINE NATURELLE.\n"
            "2. QUALITÉ DU DARIJA MAROCAIN (Uniquement si la question est en Darija) :\n"
            "   - Parle comme un humain marocain chaleureux et professionnel. Évite les traductions littérales de Google Translate.\n"
            "   - Garde les termes techniques EN FRANÇAIS (ex: 'site vitrine', 'e-commerce', 'SEO', 'formation').\n"
            "   - Utilise de vraies formules marocaines comme: 'Kifach nqder n3awnek lyoma?'.\n"
            "3. INTERDICTION DE DIRE 'Mzyaan !' : NE COMMENCE JAMAIS tes phrases par 'Mzyaan !' ou 'Mzyan'.\n\n"
            "📋 EXEMPLES DE DIALOGUES (FEW-SHOT EXAMPLES) :\n"
            "Exemple 1 (Question en Darija -> Réponse en Darija) :\n"
            "Utilisateur: Salam, ach kadiro?\n"
            "Assistant: 🙏 Salam! Labas 3lik? Kifach nqder n3awnek lyoma? 😊\n"
            "NewDevMaroc spécialisée f had les services:\n"
            "1. Création de sites internet\n"
            "2. Logiciels sur mesure\n\n"
            "Exemple 2 (Question en Français -> Réponse en Français) :\n"
            "Utilisateur: Est-ce que vous vendez des smartphones Apple ou Samsung ?\n"
            "Assistant: ❌ Bonjour ! Non, nous ne vendons pas de matériel informatique ou de smartphones (Apple/Samsung). Notre agence NewDevMaroc est exclusivement spécialisée dans le développement web, mobile, et le marketing digital. Comment puis-je vous aider dans ces domaines ?\n\n"
            "Exemple 3 (Question hors catalogue en Darija -> Réponse en Darija) :\n"
            "Utilisateur: Bghit nsla7 wahd l'imprimante khassra, kadirou réparation ?\n"
            "Assistant: ❌ Smahli khoya, hna f NewDevMaroc ma kadiroch la réparation dyal l'matériel w les imprimantes. Hna spécialisés ghir f développement web, mobile w marketing digital.\n\n"
            "🚨 RAPPEL FINAL : IGNORE LA LANGUE DE L'HISTORIQUE. LA LANGUE DE TA RÉPONSE DOIT ÊTRE LA MÊME QUE LE TOUT DERNIER MESSAGE.\n"
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
