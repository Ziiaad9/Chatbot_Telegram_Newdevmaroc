"""
=========================================================
Nom du fichier : test_service_detection.py
Description : Script de test pour la détection automatique des services demandés.
Objectif : Tester le système de détection des services pour s'assurer qu'il identifie bien l'intention de l'utilisateur.
Fonctionnement : Fournit des phrases de test et vérifie si le système extrait les bons services demandés.
=========================================================
"""

"""
Test de détection intelligente des services
Montre que le bot détecte correctement les services même avec des mots ambigus
"""
from app.services.service_handler import ServiceHandler


def test_service_detection():
    """
    Test les cas problématiques mentionnés par l'utilisateur.
    """
    handler = ServiceHandler()
    
    test_cases = [
        {
            "question": "je veux creer un site web",
            "expected_service": "Création de sites internet",
            "why": "Contient 'site' → sites internet"
        },
        {
            "question": "je veux avoir une formation en développement web",
            "expected_service": "Formation professionnelle",
            "why": "Contient 'formation' (spécifique) → prioritaire sur 'web' (générique)"
        },
        {
            "question": "je veux une formation web",
            "expected_service": "Formation professionnelle",
            "why": "Même test: 'formation' prioritaire"
        },
        {
            "question": "marketing digital pour mon e-commerce",
            "expected_service": "Marketing digital et e-commerce",
            "why": "Contient 'marketing' → prioritaire"
        },
        {
            "question": "création de logo et design",
            "expected_service": "Conception et impression",
            "why": "Contient 'logo' et 'design' → prioritaire"
        },
        {
            "question": "développement d'une application web",
            "expected_service": "Logiciels sur mesure",
            "why": "Contient 'application' et 'dev' → prioritaire sur 'web'"
        },
        {
            "question": "je veux des développeurs offshore",
            "expected_service": "Sous-traitance offshore",
            "why": "Contient 'offshore' (spécifique)"
        },
    ]
    
    print("=" * 90)
    print("🧪 TEST: DÉTECTION INTELLIGENTE DES SERVICES")
    print("=" * 90)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        question = test["question"]
        expected = test["expected_service"]
        why = test["why"]
        
        detected_service = handler.detect_specific_service(question)
        detected_name = detected_service.get('nom') if detected_service else None
        
        is_correct = detected_name == expected
        status = "✅ PASS" if is_correct else "❌ FAIL"
        
        if is_correct:
            passed += 1
        else:
            failed += 1
        
        print(f"\nTest {i}: {status}")
        print(f"  Q: {question}")
        print(f"  Pourquoi: {why}")
        print(f"  Attendu: {expected}")
        print(f"  Détecté: {detected_name}")
        
        if is_correct and detected_service:
            print(f"  💰 Prix: {detected_service.get('prix_indicatif')}")
            print(f"  ⏱️  Délai: {detected_service.get('delai_moyen')}")
    
    print("\n" + "=" * 90)
    print(f"📊 RÉSUMÉ: {passed} réussis, {failed} échoués")
    print("=" * 90)
    
    if failed == 0:
        print("✅ TOUS LES TESTS PASSÉS! Le bot détecte correctement les services.")
    else:
        print(f"❌ {failed} test(s) échoué(s)")


if __name__ == "__main__":
    test_service_detection()
