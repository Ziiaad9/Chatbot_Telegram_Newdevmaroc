"""
=========================================================
Nom du fichier : service_handler.py
Description : Gestion de la logique spécifique aux différents services proposés.
Objectif : Gérer la logique spécifique liée aux services de l'entreprise.
Fonctionnement : Contient les algorithmes et règles métiers pour traiter les demandes spécialisées concernant les offres.
=========================================================
"""

"""
Smart handler pour les questions concernant les services.
Détecte les questions sur les services et retourne les données réelles du backend.
"""
from app.ai.knowledge_base_loader import KnowledgeBase
from app.utils.logger import logger


class ServiceHandler:
    """Gère les questions sur les services en retournant les données réelles."""
    
    def __init__(self):
        self.kb = KnowledgeBase()
    
    def detect_specific_service(self, user_message: str) -> dict | None:
        """
        Détecte si l'utilisateur demande des infos sur UN service spécifique.
        Retourne le service trouvé ou None.
        
        Utilise une stratégie de détection INTELLIGENTE:
        1. Cherche d'abord les MOTS-CLÉS SPÉCIFIQUES (formation, marketing, logo, etc.)
        2. Puis cherche les mots-clés GÉNÉRIQUES (web, dev, etc.)
        3. Cherche le nom du service directement
        """
        message_lower = user_message.lower()
        services = self.kb.get_all_services()
        
        # === ÉTAPE 1: MOTS-CLÉS SPÉCIFIQUES (haute priorité) ===
        # Ces mots sont très spécifiques à un service particulier
        specific_keywords_map = {
            # Formation professionnelle
            "formation": "Formation professionnelle",
            "training": "Formation professionnelle",
            "cours": "Formation professionnelle",
            "learning": "Formation professionnelle",
            
            # Marketing digital
            "marketing": "Marketing digital et e-commerce",
            "ads": "Marketing digital et e-commerce",
            "publicité": "Marketing digital et e-commerce",
            "campagne": "Marketing digital et e-commerce",
            "community": "Marketing digital et e-commerce",
            "seo": "Marketing digital et e-commerce",
            
            # Design et impression
            "logo": "Conception et impression",
            "design": "Conception et impression",
            "graphique": "Conception et impression",
            "impression": "Conception et impression",
            "branding": "Conception et impression",
            "identité visuelle": "Conception et impression",
            
            # Offshore
            "offshore": "Sous-traitance offshore",
            "développeurs": "Sous-traitance offshore",
            "régie": "Sous-traitance offshore",
            "prestataire": "Sous-traitance offshore",
        }
        
        # Chercher les mots-clés spécifiques EN PREMIER (haute priorité)
        for keyword, service_name in specific_keywords_map.items():
            if keyword in message_lower:
                return self.kb.get_service_by_name(service_name)
        
        # === ÉTAPE 2: MOTS-CLÉS GÉNÉRIQUES (basse priorité) ===
        generic_keywords_map = {
            "site": "Création de sites internet",
            "web": "Création de sites internet",
            "e-commerce": "Création de sites internet",
            "ecommerce": "Création de sites internet",
            "vitrine": "Création de sites internet",
            "logiciel": "Logiciels sur mesure",
            "app": "Logiciels sur mesure",
            "application": "Logiciels sur mesure",
            "dev": "Logiciels sur mesure",
            "développement": "Logiciels sur mesure",
        }
        
        for keyword, service_name in generic_keywords_map.items():
            if keyword in message_lower:
                return self.kb.get_service_by_name(service_name)
        
        # === ÉTAPE 3: Recherche directe par nom de service ===
        for service in services:
            service_name_lower = service.get('nom', '').lower()
            if service_name_lower in message_lower:
                return service
        
        return None
    
    def format_service_response(self, service: dict) -> str:
        """
        Formate une réponse intelligente pour un service spécifique.
        """
        response = f"📌 **{service.get('nom')}**\n\n"
        response += f"📝 **Description:**\n{service.get('description')}\n\n"
        response += f"💰 **Prix indicatif:**\n{service.get('prix_indicatif')}\n\n"
        response += f"⏱️ **Délai moyen:**\n{service.get('delai_moyen')}\n\n"
        response += f"➡️ Pour plus de détails et un devis personnalisé:\n"
        response += f"📧 Contactez-nous: {self.kb.get_contact()}\n"
        response += f"ou tapez `/contact` 📞"
        return response
    
    def is_generic_service_query(self, user_message: str) -> bool:
        """
        Détecte si le message demande la LISTE de tous les services.
        Retourne True pour les demandes génériques, False pour les questions spécifiques.
        
        Exemples:
        - "Quelle sont les services?" → True (liste tous)
        - "Kader dyal services?" → True (liste tous)
        - "Quel est le prix d'une Formation?" → False (question spécifique, passe au LLM)
        - "Proposez-vous du web?" → False (question spécifique, passe au LLM)
        """
        message_lower = user_message.lower()
        
        # Mots-clés qui indiquent une demande de LISTE
        list_keywords = [
            "liste",
            "list",
            "tous",
            "all",
            "complet",
            "complete",
            "services",  # juste "services" seul
            "kader",  # darija: services
            "kayna", # darija: what do you have
            "shnu kayna", # darija: what do you have
            "proposez",  # what do you propose
            "propose",
            "offrez",
            "offre",
            "offer",
            "diri",  # darija: tell me
            "dlini"  # darija: tell me
        ]
        
        # Mots-clés qui indiquent une question SPÉCIFIQUE
        specific_keywords = [
            "prix",
            "price",
            "cost",
            "delai",
            "delay",
            "combien",
            "how much",
            "quand",
            "when",
            "comment",
            "how",
            "pourquoi",
            "why",
            "besoin",
            "need",
            "veut",
            "want",
            "faut",
            "require",
            "khass",  # darija: need
            "kaynin",  # darija: are there
            "ila"  # darija: if
        ]
        
        # Si le message contient des mots de question spécifique → question spécifique
        for keyword in specific_keywords:
            if keyword in message_lower:
                return False
        
        # Sinon, vérifier les mots-clés de liste
        for keyword in list_keywords:
            if keyword in message_lower:
                return True
        
        return False
    
    def get_services_response(self, user_message: str) -> str:
        """
        Retourne une réponse formatée avec les services disponibles.
        """
        services = self.kb.get_all_services()
        contact = self.kb.get_contact()
        
        # Construction du message
        response = "🎯 **Nos services NewDevMaroc:**\n\n"
        
        for idx, service in enumerate(services, 1):
            response += f"**{idx}. {service.get('nom')}**\n"
            response += f"   📝 {service.get('description')}\n"
            response += f"   💰 Prix: {service.get('prix_indicatif')}\n"
            response += f"   ⏱️  Délai moyen: {service.get('delai_moyen')}\n\n"
        
        response += f"➡️ Pour plus de détails ou un devis personnalisé, contactez-nous:\n"
        response += f"📧 {contact}\n"
        response += f"ou tapez `/contact` pour nous écrire directement! 📞"
        
        return response
    
    def handle_service_inquiry(self, user_message: str) -> str | None:
        """
        Gère une question sur les services avec VRAIE intelligence.
        
        Stratégie:
        1. Si c'est une demande CLAIRE de LISTE → retourne la liste
        2. Si c'est une question TRÈS SPÉCIFIQUE sur un service (prix, délai) → retourne le service
        3. Sinon → retourne None pour que le LLM handle avec contexte service
        
        Le LLM aura l'info du service injecté dans son contexte pour répondre intelligemment.
        """
        # NIVEAU 1: Demande générique de LISTE
        if self.is_generic_service_query(user_message):
            logger.info(f"Generic service list request: {user_message}")
            return self.get_services_response(user_message)
        
        # NIVEAU 2: Question TRÈS SPÉCIFIQUE sur UN service
        # Chercher un service seulement si on a des mots de QUESTION spécifique (prix, délai, etc.)
        message_lower = user_message.lower()
        
        # Mots qui indiquent une question SPÉCIFIQUE sur les détails
        specific_question_keywords = [
            "prix",
            "price",
            "cost",
            "coûte",
            "delai",
            "delay",
            "combien",
            "how much",
            "quand",
            "when",
            "tarif",
            "tariff"
        ]
        
        # Si le message contient une question spécifique (prix, délai, etc.)
        has_specific_question = any(kw in message_lower for kw in specific_question_keywords)
        
        if has_specific_question:
            specific_service = self.detect_specific_service(user_message)
            if specific_service:
                logger.info(f"Specific service question detected: {specific_service.get('nom')} - {user_message}")
                return self.format_service_response(specific_service)
        
        # NIVEAU 3: Questions générales ou mixtes
        # Laisser le LLM répondre, mais il aura le contexte du service dans le system prompt
        logger.info(f"General question, passing to LLM with potential service context: {user_message}")
        return None
