"""
=========================================================
Nom du fichier : knowledge_base_loader.py
Description : Chargement et traitement de la base de connaissances (documents, données).
Objectif : Charger les informations de l'entreprise (services, prix) pour que l'IA puisse les utiliser.
Fonctionnement : Lit des documents ou des données structurées et les prépare pour être injectés dans la base vectorielle.
=========================================================
"""

import json
from pathlib import Path
from app.utils.logger import logger

class KnowledgeBase:
    _instance = None
    _data = None
    
    def __new__(cls):
        """Singleton pattern pour charger une seule fois."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Charger la base de connaissances depuis le fichier JSON."""
        if self._data is None:
            try:
                kb_path = Path(__file__).parent.parent / "db" / "knowledge_base.json"
                with open(kb_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                logger.info("Base de connaissances chargée avec succès.")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de la base de connaissances: {e}")
                self._data = {}
                
    def reload(self):
        """Recharge la base de connaissances depuis le fichier."""
        self._data = None
        self.__init__()
    
    def get_all_services(self) -> list:
        """Retourne tous les services."""
        return self._data.get("services", [])
    
    def get_service_by_name(self, service_name: str) -> dict | None:
        """Trouve un service par son nom (recherche partielle)."""
        services = self.get_all_services()
        service_name_lower = service_name.lower()
        for service in services:
            if service_name_lower in service.get("nom", "").lower():
                return service
        return None
    
    def get_service_names(self) -> list:
        """Retourne la liste des noms de services."""
        return [s.get("nom") for s in self.get_all_services()]
    
    def get_contact(self) -> str:
        """Retourne le mail de contact."""
        return self._data.get("contact", "contact@newdevmaroc.com")
        
    def get_telephone(self) -> str:
        """Retourne le numéro de téléphone."""
        return self._data.get("telephone", "05 35 65 07 57")
    
    def get_entreprise(self) -> str:
        """Retourne le nom de l'entreprise."""
        return self._data.get("entreprise", "NewDevMaroc")
    
    def get_regles_chatbot(self) -> list:
        """Retourne les règles du chatbot."""
        return self._data.get("regles_chatbot", [])
    
    def format_services_list(self) -> str:
        """Formate la liste des services pour afficher au chatbot."""
        services = self.get_all_services()
        formatted = "Nos services:\n\n"
        for service in services:
            formatted += f"• {service.get('nom')}\n"
            formatted += f"  Description: {service.get('description')}\n"
            formatted += f"  Prix: {service.get('prix_indicatif')}\n"
            formatted += f"  Délai moyen: {service.get('delai_moyen')}\n\n"
        return formatted
