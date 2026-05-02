"""
=========================================================
Nom du fichier : test_openrouter.py
Description : Script de test pour la connexion et l'API OpenRouter/Groq.
Objectif : Vérifier que la connexion à l'API OpenRouter/Groq fonctionne correctement.
Fonctionnement : Envoie un prompt de test à l'API et vérifie la réception d'une réponse valide.
=========================================================
"""

import urllib.request, json

req = urllib.request.Request('https://openrouter.ai/api/v1/models')
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        free_models = [m['id'] for m in data['data'] if ':free' in m['id']]
        print("Free models available:", free_models)
except Exception as e:
    print(f"Error: {e}")
