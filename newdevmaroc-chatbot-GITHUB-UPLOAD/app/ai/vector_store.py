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
        
        # Ajouter les infos générales
        adresse = data.get('adresse', '')
        horaires = data.get('horaires', {})
        horaires_text = f"Lundi-Vendredi: {horaires.get('lundi_vendredi', '')}, Samedi: {horaires.get('samedi', '')}, Dimanche: {horaires.get('dimanche', '')}"
        general_info = f"L'entreprise s'appelle {data.get('entreprise', 'NewDevMaroc')}. Contact: {data.get('contact', '')}. Téléphone: {data.get('telephone', '')}. Adresse: {adresse}. Horaires d'ouverture: {horaires_text}."
        documents.append(Document(page_content=general_info, metadata={"source": "general_info"}))
        
        # Ajouter les règles du chatbot
        regles = " ".join(data.get("regles_chatbot", []))
        documents.append(Document(page_content=f"Règles du chatbot: {regles}", metadata={"source": "rules"}))
        
        # Ajouter chaque service comme un document distinct (chunk)
        for service in data.get("services", []):
            content = f"Service: {service['nom']}\nDescription: {service['description']}\nPrix indicatif: {service['prix_indicatif']}\nDélai moyen: {service['delai_moyen']}"
            documents.append(Document(page_content=content, metadata={"source": "service", "name": service['nom']}))

        # Créer le vector store ChromaDB
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
    def get_retriever(self):
        """Retourne le retriever pour la chaîne RAG"""
        if self.vector_store is None:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        # On augmente 'k' à 10 pour s'assurer que tous les services (6) + les infos générales 
        # soient récupérés quand l'utilisateur demande "quels sont vos services"
        return self.vector_store.as_retriever(search_kwargs={"k": 10})

if __name__ == "__main__":
    print("Initialisation de la base vectorielle ChromaDB...")
    manager = VectorStoreManager()
    manager.initialize_db()
    print("Terminé ! Les données sont vectorisées et stockées dans data/chroma_db/")
