1. creeer lenv de dev python: `python3.12 -mvenv atm_env`
2. Installer les deps: `pip install -r requirements.txt`
3. Se positionner dans le repertoir app/ et Lancer le service sur le port 8001:
   ```bash
   cd app
   uvicorn main:app --reload --port=8001
   ```
4. paramétrage des ports:
 install: python-dotenv
 pour modifier les ports il faut se référer au fichier .env dans la racine du répertoire  de backend 
5. pour lancer les service faut activer l'env de dev et se positionner dans le répertoire app/
```bash
   cd app
   python main.py
   ```
