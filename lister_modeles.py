import os
from google import genai

# On récupère ta clé API depuis le terminal
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("N'oublie pas de faire un 'export API_KEY=ta_cle' avant de lancer le script.")

# On initialise le client
client = genai.Client(api_key=API_KEY)

print("Recherche des modèles disponibles...\n")

# On boucle sur la liste des modèles fournis par l'API
for model in client.models.list():
    print(f"Nom exact du modèle : {model.name}")
    print(f"Description : {model.display_name}")
    print("-" * 40)