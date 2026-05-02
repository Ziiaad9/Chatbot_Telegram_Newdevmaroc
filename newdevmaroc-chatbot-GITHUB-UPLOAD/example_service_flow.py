"""
=========================================================
Nom du fichier : example_service_flow.py
Description : Exemple de flux de service (simulation des étapes d'un service).
Objectif : Illustrer le flux complet de traitement d'un service spécifique.
Fonctionnement : Exécute une série d'étapes prédéfinies pour simuler la fourniture d'un service (ex: devis).
=========================================================
"""

"""
Exemple de test: Comment le bot répond aux questions sur les services
"""
import asyncio
from app.services.service_handler import ServiceHandler
from app.ai.knowledge_base_loader import KnowledgeBase


def test_service_queries():
    """
    Démontre comment le bot détecte et répond aux questions sur les services.
    """
    handler = ServiceHandler()
    
    # Exemples de questions que les utilisateurs peuvent poser
    test_questions = [
        "Quelle sont les services que vous offrez?",
        "Kader dyal services?",  # Darija: What services?
        "Diri chi hawajat?",  # Darija: Tell me something
        "Proposez-vous du web?",
        "Services e-commerce?",
        "Vous offrez une formation?",
        "Bonjour comment ça va?",  # NOT a service query
        "Logo et design?",
    ]
    
    print("=" * 70)
    print("EXEMPLE: Comment le bot détecte les questions sur les services")
    print("=" * 70)
    
    for question in test_questions:
        is_service = handler.is_service_query(question)
        print(f"\nQ: {question}")
        print(f"   Service Query? {is_service}")
        
        if is_service:
            response = handler.handle_service_inquiry(question)
            print(f"   ✅ Bot responds with:")
            print("   " + "\n   ".join(response.split("\n")[:5]) + "...")
    
    print("\n" + "=" * 70)
    print("BACKEND DATA (Knowledge Base)")
    print("=" * 70)
    
    kb = KnowledgeBase()
    print(f"\n📌 Company: {kb.get_entreprise()}")
    print(f"📧 Contact: {kb.get_contact()}")
    print(f"\n📋 Services disponibles: {len(kb.get_all_services())}")
    for idx, service in enumerate(kb.get_all_services(), 1):
        print(f"\n   {idx}. {service['nom']}")
        print(f"      Prix: {service['prix_indicatif']}")


if __name__ == "__main__":
    test_service_queries()
