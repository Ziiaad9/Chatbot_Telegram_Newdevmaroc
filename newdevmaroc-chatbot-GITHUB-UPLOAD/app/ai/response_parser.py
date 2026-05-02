"""
=========================================================
Nom du fichier : response_parser.py
Description : Analyse et structuration des réponses générées par l'IA.
Objectif : Formater et extraire des informations utiles à partir du texte brut renvoyé par l'IA.
Fonctionnement : Analyse la réponse de l'IA (parfois en JSON) et la convertit en structures de données utilisables par le bot.
=========================================================
"""

"""
Parse et formate les réponses du LLM.
Si le LLM échoue, fournit des réponses intelligentes de fallback.
"""
from app.ai.knowledge_base_loader import KnowledgeBase


def parse_llm_response(raw_response: str | None) -> str:
    """
    Nettoie et formate la réponse du LLM.
    
    Si raw_response est valide → retourne la réponse du LLM
    Si raw_response est None → fournit une réponse intelligente de fallback
    """
    if raw_response:
        return raw_response.strip()
    
    # Fallback intelligentes - le bot donne toujours une réponse utile
    kb = KnowledgeBase()
    contact = kb.get_contact()
    
    fallback_response = (
        "Je rencontre actuellement un léger problème technique pour traiter votre demande en détail. 🔧\n\n"
        "Cependant, voici ce que je peux vous proposer:\n\n"
        "✅ **Tapez `/services`** pour voir la liste complète de nos services\n"
        "✅ **Tapez `/contact`** pour nous écrire directement\n"
        "✅ **Écrivez-nous** sur 📧 **{contact}**\n\n"
        "Nous vous répondrons rapidement! 😊"
    ).format(contact=contact)
    
    return fallback_response
