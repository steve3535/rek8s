1. creeer lenv de dev python: `python3.12 -mvenv atm_env`
2. Installer les deps: `pip install -r requirements.txt`
3. Se positionner dans le repertoir app/ et Lancer le service sur le port 8001:
   ```bash
   cd app
   uvicorn main:app --reload --port=8001
   ```
