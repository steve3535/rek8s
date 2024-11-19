### changements
* le Dockerfile utilise nodejs et nginx pour pouvoir generer le config.js au build du conteneur
* il nest theoriquement plus besoin de conteneuriser les autres services parcke les requetes tournent depuis le browser

1. se positionner a la racine du projet  
2. `docker build -f frontend/Dockerfile -t frontend .`  
3. `docker run --name frontend -p 8088:80 -d frontend`  (8088 etant un choix arbitraire)  
