# Utiliser une image de base
FROM python:3.10

# Définir un répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du projet dans l'image
COPY ./app .

# Définir un argument de build pour le port
ARG PORT_NI

# Exposer le port pour l'application
EXPOSE ${PORT_NI}

# Définir une variable d'environnement pour le port
ENV PORT=${PORT_NI}

# Lancer l'application
CMD ["python", "main.py"]
