"""
=========================================================
Nom du fichier : config.py
Description : Configuration globale de l'application (variables d'environnement, paramètres).
Objectif : Centraliser toute la configuration et les variables d'environnement de l'application.
Fonctionnement : Utilise `pydantic_settings` pour lire le fichier `.env` et exposer les paramètres (clés API, configuration DB) au reste de l'application.
=========================================================
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Configuration de l'application via les variables d'environnement.
    """
    TELEGRAM_BOT_TOKEN: str
    OPENROUTER_API_KEY: str
    GROQ_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"  # Changed to gpt-4o-mini for reliability
    
    # On parse les IDs administrateur comme une liste d'entiers
    ADMIN_USER_IDS: str = ""
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/chatbot.db"
    MAX_HISTORY_MESSAGES: int = 10
    RATE_LIMIT_MAX: int = 20
    RATE_LIMIT_WINDOW: int = 3600
    
    BOT_SYSTEM_PROMPT: str = (
        "Tu es l'assistant virtuel de NewDevMaroc 🇲🇦, une agence spécialisée en création "
        "de sites web, développement web et solutions digitales au Maroc.\n\n"
        
        "SERVICES PROPOSÉS:\n"
        "1. Création de sites internet (vitrines & e-commerce)\n"
        "2. Logiciels sur mesure\n"
        "3. Marketing digital et e-commerce\n"
        "4. Formation professionnelle\n"
        "5. Sous-traitance offshore\n"
        "6. Conception et impression\n\n"
        
        "INSTRUCTIONS IMPORTANTES:\n"
        "- Toujours être professionnel, chaleureux et répondre en français ou darija selon la langue du client\n"
        "- Si le client demande un service, POSE DES QUESTIONS PERTINENTES pour comprendre ses besoins:\n"
        "  * Pour un site: Type de site? Nombre de pages? Fonctionnalités spéciales? Design preferences?\n"
        "  * Pour un logiciel: Quel type d'application? Quels processus automatiser? Integrations nécessaires?\n"
        "  * Pour marketing: Quel budget? Quels réseaux? Quel public cible?\n"
        "- JAMAIS donner de prix définitif - ces sont des estimations uniquement\n"
        "- Si le client demande un prix, donne l'estimation mais dis que c'est indicatif\n"
        "- Si le client demande les délais, donne l'info mais explique que ça dépend de la complexité\n"
        "- Propose toujours un appel ou email pour un devis précis: contact@newdevmaroc.com\n"
        "- Si le service demandé n'existe pas dans notre catalogue, dit poliment qu'on le propose pas\n\n"
        
        "RÈGLES DE CONVERSATION:\n"
        "- Pose des questions naturelles et pertinentes, pas robotiques\n"
        "- Utilise les emojis pour rendre la conversation plus agréable\n"
        "- Récapitule ce que le client veut avant de proposer une solution\n"
        "- Soit empathique et à l'écoute des besoins du client\n"
    )
    
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def admin_ids_list(self) -> List[int]:
        """Retourne la liste des IDs administrateurs en entiers."""
        if not self.ADMIN_USER_IDS:
            return []
        return [int(uid.strip()) for uid in self.ADMIN_USER_IDS.split(",") if uid.strip().isdigit()]

# Instance globale des paramètres
settings = Settings()
