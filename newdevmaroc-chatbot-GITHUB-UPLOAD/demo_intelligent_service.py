"""
=========================================================
Nom du fichier : demo_intelligent_service.py
Description : Démo du service intelligent pour les interactions utilisateur.
Objectif : Montrer comment le service intelligent traite les demandes des utilisateurs.
Fonctionnement : Initialise le système d'IA et fait une démonstration de ses réponses sur des cas de test.
=========================================================
"""

"""
Demo: Intelligent Service Detection and Response
Montre comment le bot répond intelligemment aux questions sur les services
"""
from app.services.service_handler import ServiceHandler
from app.ai.knowledge_base_loader import KnowledgeBase


def demo_intelligent_responses():
    """
    Démontre comment le bot détecte les questions spécifiques et répond intelligemment.
    """
    handler = ServiceHandler()
    kb = KnowledgeBase()
    
    print("=" * 80)
    print("🤖 DÉMO: BOT INTELLIGENT AVEC DÉTECTION DE SERVICES")
    print("=" * 80)
    
    # Scénarios de test
    test_cases = [
        {
            "question": "Quelle sont les services que vous offrez?",
            "type": "LISTE COMPLÈTE",
            "expected": "Retourne la liste de tous les services"
        },
        {
            "question": "Quel est le prix d'une Formation en développement web?",
            "type": "SERVICE SPÉCIFIQUE",
            "expected": "Retourne les infos sur la Formation"
        },
        {
            "question": "Combien ça coûte pour un site e-commerce?",
            "type": "SERVICE SPÉCIFIQUE",
            "expected": "Retourne les infos sur Création de sites internet"
        },
        {
            "question": "Vous faites du développement de logiciels?",
            "type": "SERVICE SPÉCIFIQUE",
            "expected": "Retourne les infos sur Logiciels sur mesure"
        },
        {
            "question": "Quel délai pour une formation?",
            "type": "SERVICE SPÉCIFIQUE",
            "expected": "Retourne les infos sur Formation"
        },
        {
            "question": "Proposez-vous du design graphique?",
            "type": "LISTE COMPLÈTE",
            "expected": "Retourne la liste (ou service spécifique si détecté)"
        }
    ]
    
    print("\n📋 SCÉNARIOS DE TEST:\n")
    
    for i, test in enumerate(test_cases, 1):
        question = test["question"]
        test_type = test["type"]
        
        print(f"\n{'─' * 80}")
        print(f"Test {i}: {test_type}")
        print(f"{'─' * 80}")
        print(f"Q: {question}")
        
        # Détection du service spécifique
        specific_service = handler.detect_specific_service(question)
        
        # Détection de la liste générique
        is_generic = handler.is_generic_service_query(question)
        
        print(f"\n✓ Service spécifique détecté: {specific_service.get('nom') if specific_service else 'None'}")
        print(f"✓ Demande générique? {is_generic}")
        
        # Réponse
        response = handler.handle_service_inquiry(question)
        if response:
            # Afficher les 3 premières lignes de la réponse
            lines = response.split("\n")[:3]
            print(f"\n📢 Réponse du bot (aperçu):")
            for line in lines:
                print(f"   {line}")
        else:
            print(f"\n📢 Réponse: Passé au LLM pour réponse personnalisée")
    
    print("\n\n" + "=" * 80)
    print("📊 RÉSUMÉ DES SERVICES DISPONIBLES")
    print("=" * 80)
    
    services = kb.get_all_services()
    for i, service in enumerate(services, 1):
        print(f"\n{i}. {service['nom']}")
        print(f"   💰 Prix: {service['prix_indicatif']}")
        print(f"   ⏱️  Délai: {service['delai_moyen']}")


if __name__ == "__main__":
    demo_intelligent_responses()
