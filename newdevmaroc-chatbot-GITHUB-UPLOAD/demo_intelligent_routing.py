"""
=========================================================
Nom du fichier : demo_intelligent_routing.py
Description : Démo du routage intelligent des requêtes utilisateur.
Objectif : Démontrer le fonctionnement du routage intelligent pour séparer les différents types de requêtes.
Fonctionnement : Le script simule l'envoi de requêtes et affiche vers quel service (IA, base de données, etc.) elles sont dirigées.
=========================================================
"""

"""
Démonstration: Intelligence vs Service Detection
Montre comment le bot différencie les questions et répond intelligemment
"""
from app.services.service_handler import ServiceHandler
from app.ai.prompt_builder import build_messages_payload
from app.db.models import Message


def demo_intelligent_routing():
    """
    Démontre le nouveau système de routing intelligent.
    """
    handler = ServiceHandler()
    
    print("=" * 90)
    print("🤖 DÉMO: BOT AVEC INTELLIGENCE - SERVICE VS CONVERSATION")
    print("=" * 90)
    
    scenarios = [
        {
            "category": "🎯 SERVICE QUERY - Liste complète",
            "question": "Quelle sont les services que vous offrez?",
            "expected_route": "Retourne la LISTE du backend (pas LLM)",
            "will_bypass_llm": True
        },
        {
            "category": "🎯 SERVICE QUERY - Prix/Délai",
            "question": "Quel est le prix d'une formation en développement?",
            "expected_route": "Retourne INFO SERVICE (pas LLM)",
            "will_bypass_llm": True
        },
        {
            "category": "💬 GENERAL QUESTION - Identité",
            "question": "C'est le chatbot de NewDevMaroc? Qu'est-ce que c'est?",
            "expected_route": "Va au LLM pour répondre intelligemment",
            "will_bypass_llm": False
        },
        {
            "category": "💬 GENERAL QUESTION - Salutation",
            "question": "Bonjour! Comment ça va?",
            "expected_route": "Va au LLM pour conversation",
            "will_bypass_llm": False
        },
        {
            "category": "💬 GENERAL QUESTION - Demande spécifique",
            "question": "Vous faites des sites web?",
            "expected_route": "Va au LLM (pas 'prix/délai')",
            "will_bypass_llm": False
        },
        {
            "category": "🎯 SERVICE QUERY - Détail spécifique",
            "question": "Combien ça coûte pour un logiciel sur mesure?",
            "expected_route": "Retourne INFO du service",
            "will_bypass_llm": True
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        question = scenario["question"]
        category = scenario["category"]
        expected = scenario["expected_route"]
        will_bypass = scenario["will_bypass_llm"]
        
        print(f"\n{'─' * 90}")
        print(f"Scénario {i}: {category}")
        print(f"{'─' * 90}")
        print(f"Q: {question}\n")
        
        # Tester le routing
        response = handler.handle_service_inquiry(question)
        
        if response:
            print(f"✅ BYPASS LLM - Réponse du backend:")
            lines = response.split("\n")[:2]
            for line in lines:
                print(f"   {line}")
            print(f"   ...")
        else:
            print(f"🔄 PASSE AU LLM - {expected}")
        
        # Vérifier si le comportement est correct
        bypassed_llm = response is not None
        is_correct = bypassed_llm == will_bypass
        
        print(f"\n✓ Résultat: {'CORRECT ✅' if is_correct else 'ERREUR ❌'}")
        print(f"  Attendu: LLM bypass = {will_bypass}")
        print(f"  Réel: LLM bypass = {bypassed_llm}")
    
    print("\n" + "=" * 90)
    print("📌 RÉSUMÉ DE LA LOGIQUE INTELLIGENTE")
    print("=" * 90)
    print("""
✅ SERVICE QUERIES (Bypass LLM):
   - Demandes de liste générique: "services", "liste complète"
   - Questions avec "prix", "délai", "coûte", "combien"

💬 GENERAL QUERIES (Use LLM):
   - Questions sur l'identité: "qui êtes-vous", "c'est quoi"
   - Salutations et conversations
   - Questions générales sur les services (sans prix/délai)
   
🧠 LLM reçoit le contexte:
   - Si l'utilisateur parle d'un service → contexte du service injecté
   - LLM peut répondre intelligemment avec les détails du service
    """)


if __name__ == "__main__":
    demo_intelligent_routing()
