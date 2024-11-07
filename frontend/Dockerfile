
FROM python:3.10-slim

# Définir le répertoire de travail  du conteneur
WORKDIR /app

# Copie de tous les fichiers  dans le conteneur
COPY . .

# Exposer le port sur lequel le serveur HTTP Python écoutera
EXPOSE 8080

# Commande pour démarrer le serveur HTTP
CMD ["python", "-m", "http.server", "8080"]
