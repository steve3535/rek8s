### changements
* le Dockerfile utilise nodejs et nginx pour pouvoir generer le config.js au build du conteneur
* il nest theoriquement plus besoin de conteneuriser les autres services parcke les requetes tournent depuis le browser

1. se positionner a la racine du projet 
2. creer le fichier .env sur la racine de rek8s(les variables etant un choix arbitraire)
` PORT_ATM=8001
  PORT_NI=8002
  PORT_BANKING=8000
  RECO_WEB_PORT=8080
`
2. `docker-compose  up --build -d`  
3. `docker-compose ps ou docker ps`
4. dans le navigateur: localhost:8080
