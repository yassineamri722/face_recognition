# Utilise une image Python 3.8 de base
FROM python:3.8-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers locaux dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port pour l'application Flask
EXPOSE 5000

# Démarrer l'application Flask
CMD ["python", "app.py"]
