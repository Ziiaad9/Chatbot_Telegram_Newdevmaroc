# Utilise l'image Python 3.11 légère
FROM python:3.11-slim

# Configure des variables d'environnement utiles pour Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installe les dépendances système minimales (si besoin)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Définie le répertoire de travail
WORKDIR /app

# Copie d'abord les requirements pour utiliser le cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste de l'application
COPY . .

# Création du dossier pour la base de données
RUN mkdir -p /app/data

# Le point d'entrée par défaut
CMD ["python", "app/main.py"]
