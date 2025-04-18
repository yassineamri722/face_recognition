# Étape 1 : Utilisation de l'image Python slim
FROM python:3.10-slim

# Étape 2 : Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Étape 4 : Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier tout le contenu du projet dans le conteneur
COPY . /app/

# Ajouter /app/src au PYTHONPATH pour permettre à Python de trouver face_recognizer
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Étape 6 : Exposer le port 5000 sur lequel Gunicorn écoutera
EXPOSE 5000

# Étape 7 : Lancer l'application avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
