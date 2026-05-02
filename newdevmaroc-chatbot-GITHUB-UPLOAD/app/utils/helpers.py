"""
=========================================================
Nom du fichier : helpers.py
Description : Fonctions utilitaires diverses utilisées dans l'application.
Objectif : Regrouper des petites fonctions pratiques et réutilisables partout dans le code.
Fonctionnement : Contient des fonctions de formatage de texte, de validation ou d'autres opérations utilitaires simples.
=========================================================
"""

import datetime

def format_timestamp(ts: float) -> str:
    """
    Formate un timestamp POSIX en chaîne lisible.
    """
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def extract_username(user) -> str:
    """
    Extrait le nom d'utilisateur Telegram (ou First Name si absent).
    """
    if user.username:
        return f"@{user.username}"
    if user.first_name:
        return user.first_name
    return f"User_{user.id}"
