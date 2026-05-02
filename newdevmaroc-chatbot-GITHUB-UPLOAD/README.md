# NewDevMaroc Chatbot Telegram 🇲🇦🤖

Un chatbot Telegram intelligent, conçu pour **NewDevMaroc** (agence web et digitale), permettant d'interagir avec les clients via l'intelligence artificielle.

Il est construit avec **Python**, **Telegram Bot API**, **SQLite** (via SQLAlchemy async), et utilise l'API **Groq (llama3-8b-8192)** pour traiter les conversations.

## 🚀 Fonctionnalités
- Répond aux questions sur l'agence (services, tarifs, création de sites web).
- **Historique de conversation** : garde le contexte pour les derniers messages.
- **Rate limiting** : Protection intégrée en mémoire contre le spam (sans dépendance externe).
- **Interface Administrateur** : Obtenez les statistiques globales ou bannissez des utilisateurs.
- **Stockage persistant** via SQLite (fichier local `data/chatbot.db`).
- **Déploiement Dockerisé** ultra simple.

## 🏗 Architecture du projet

```text
+-------------------+      +------------------+      +----------------+
|                   |      |                  |      |                |
|  Telegram Client  +----->+  Telegram Bot    +----->+   Groq API     |
|                   |      |  (Application)   |      |   (LLM AI)     |
+-------------------+      +--------+---------+      +----------------+
                                    |
                                    v
                           +--------+---------+
                           |                  |
                           |  SQLite Database |
                           |  (Users & Msgs)  |
                           +------------------+
```

## 🛠 Prérequis potentiels
- Python 3.11+ ou Docker
- Un Token Bot Telegram (obtenu via [@BotFather](https://t.me/botfather))
- Une clé API Groq gratuite (obtenue sur [console.groq.com](https://console.groq.com))

## ⚙️ Installation Rapide (Locale)

1. **Cloner ou télécharger le projet.**
2. **Créer l'environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
4. **Configuration de l'environnement** :
   Copiez `.env.example` en `.env` et remplissez-le avec vos identifiants.
   ```bash
   cp .env.example .env
   ```
5. **Initialiser la base de données** :
   ```bash
   make init-db
   # ou: python migrations/init_db.py
   ```
6. **Lancer le bot** :
   ```bash
   make run
   # ou: python app/main.py
   ```

## 🐳 Installation avec Docker (Recommandé)

1. Configurez votre fichier `.env`.
2. Lancez simplement le `docker-compose` :
   ```bash
   make docker-up
   # ou: docker-compose up -d --build
   ```

## ⌨️ Commandes Disponibles

**Pour tous les utilisateurs :**
- `/start` : Initie le contact et enregistre l'utilisateur.
- `/help` : Affiche l'aide.
- `/reset` : Efface l'historique des conversations avec l'IA.
- `/stats` : Affiche vos statistiques d'utilisation.

**Pour les administrateurs (Configurez ADMIN_USER_IDS dans .env) :**
- `/admin_stats` : Affiche les stats complètes du bot.
- `/admin_ban <user_id>` : Bloque l'accès d'un utilisateur au bot.

## 🧰 Tests

1. Installez les dépendances de développement (`pip install -r requirements-dev.txt`)
2. Lancez pytest :
   ```bash
   make test
   ```
