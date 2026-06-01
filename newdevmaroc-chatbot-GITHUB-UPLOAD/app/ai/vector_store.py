"""
=========================================================
Nom du fichier : vector_store.py
Description : Gestion de la base de données vectorielle pour la recherche d'informations (RAG).
Objectif : Stocker et rechercher rapidement les informations pertinentes pour répondre aux questions de l'utilisateur.
Fonctionnement : Utilise des embeddings pour vectoriser le texte de la base de connaissances et effectue des recherches de similarité (recherche sémantique).
=========================================================
"""

import json
from pathlib import Path
from langchain_core.documents import Document
from langchain_chroma import Chroma
from chromadb.utils import embedding_functions

class ChromaDefaultEmbeddings:
    """Wrapper pour utiliser le modèle d'embedding gratuit et léger de ChromaDB avec LangChain."""
    def __init__(self):
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.ef(texts)
        
    def embed_query(self, text: str) -> list[float]:
        return self.ef([text])[0]

class VectorStoreManager:
    def __init__(self):
        self.persist_directory = str(Path(__file__).parent.parent / "db" / "chroma_db")
        self.embeddings = ChromaDefaultEmbeddings()
        self.vector_store = None

    def initialize_db(self):
        """Initialise ChromaDB avec les données du knowledge_base.json"""
        json_path = Path(__file__).parent.parent / "db" / "knowledge_base.json"
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        documents = []
        
        # Ajouter les infos générales avec le lexique multilingue
        adresse = data.get('adresse', '')
        horaires = data.get('horaires', {})
        horaires_text = f"Lundi-Vendredi: {horaires.get('lundi_vendredi', '')}, Samedi: {horaires.get('samedi', '')}, Dimanche: {horaires.get('dimanche', '')}"
        
        lexique = data.get("lexique", {})
        lexique_prix = ", ".join(lexique.get("prix", []))
        lexique_delai = ", ".join(lexique.get("delai", []))
        lexique_contact = ", ".join(lexique.get("contact", []))
        lexique_horaires = ", ".join(lexique.get("horaires", []))
        lexique_services = ", ".join(lexique.get("services", []))
        
        lexique_text = (
            f"Mots-clés et synonymes de prix et budget: {lexique_prix}. "
            f"Mots-clés et synonymes de temps, délai et durée: {lexique_delai}. "
            f"Mots-clés et synonymes d'adresse, contact, téléphone et localisation: {lexique_contact}. "
            f"Mots-clés et synonymes d'horaires d'ouverture: {lexique_horaires}. "
            f"Mots-clés et synonymes de services et activités: {lexique_services}."
        )
        
        general_info = f"L'entreprise s'appelle {data.get('entreprise', 'NewDevMaroc')}. Contact: {data.get('contact', '')}. Téléphone: {data.get('telephone', '')}. Adresse: {adresse}. Horaires d'ouverture: {horaires_text}. {lexique_text}"
        documents.append(Document(page_content=general_info, metadata={"source": "general_info"}))
        
        # Ajouter les règles du chatbot
        regles = " ".join(data.get("regles_chatbot", []))
        documents.append(Document(page_content=f"Règles du chatbot: {regles}", metadata={"source": "rules"}))
        
        # Ajouter chaque service comme un document distinct (chunk) enrichi de mots clés
        for service in data.get("services", []):
            mots_cles = ", ".join(service.get("mots_cles", []))
            content = f"Service: {service['nom']}\nMots-clés/Synonymes: {mots_cles}\nDescription: {service['description']}\nPrix indicatif: {service['prix_indicatif']}\nDélai moyen: {service['delai_moyen']}"
            documents.append(Document(page_content=content, metadata={"source": "service", "name": service['nom']}))

        # Créer le vector store ChromaDB
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
    def get_retriever(self):
        """Retourne le retriever pour la chaîne RAG"""
        import os
        # Auto-initialisation si le dossier n'existe pas ou est vide
        if not os.path.exists(self.persist_directory) or not os.listdir(self.persist_directory):
            from app.utils.logger import logger
            logger.info("Dossier ChromaDB absent ou vide. Initialisation automatique de la base vectorielle...")
            self.initialize_db()
        
        if self.vector_store is None:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        # On augmente 'k' à 10 pour s'assurer que tous les services (6) + les infos générales 
        # soient récupérés quand l'utilisateur demande "quels sont vos services"
        return self.vector_store.as_retriever(search_kwargs={"k": 10})

    def search_semantic(self, query: str, k: int = 4):
        """Effectue une recherche sémantique en direct et affiche les documents trouvés (pour debug)."""
        if self.vector_store is None:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        results = self.vector_store.similarity_search(query, k=k)
        print(f"\n[SEARCH] Recherche semantique pour : '{query}' (Top {k} chunks)")
        print("=" * 80)
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'N/A')
            name = doc.metadata.get('name', 'N/A')
            print(f"[{i}] Source: {source} | Nom: {name}")
            try:
                content_preview = doc.page_content.replace("\n", " | ")[:150]
                print(f"    Contenu : {content_preview}...")
            except Exception:
                print(f"    Contenu non-affichable en raison de l'encodage.")
            print("-" * 80)
        return results

if __name__ == "__main__":
    import os
    print("Initialisation/Mise a jour de la base vectorielle ChromaDB...")
    manager = VectorStoreManager()
    manager.initialize_db()
    print("Termine ! Les donnees sont vectorisees et stockees dans app/db/chroma_db/")
    
    # Test rapide de recherche sémantique
    try:
        manager.search_semantic("Quels sont les tarifs de creation de site web ?")
        manager.search_semantic("Combien de temps prend une formation ?")
    except Exception as e:
        print(f"Erreur d'affichage (encodage console) : {e}")
