# Étape 1 : Image de base
FROM python:3.10-slim

# Étape 2 : Dossier de travail
WORKDIR /app

# Étape 3 : Copier requirements.txt
COPY requirements.txt .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier tout le projet
COPY . .

# Étape 6 : Exposer le port utilisé par l'app
EXPOSE 5000

# Étape 7 : Lancer gunicorn en pointant vers src.app:app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
