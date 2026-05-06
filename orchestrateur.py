import json
import os
import subprocess
import re
import ast
import time
from google import genai

# ==========================================
# CONFIGURATION DE L'API GEMINI
# ==========================================
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("La clé API_KEY est introuvable dans les variables d'environnement.")

client = genai.Client(api_key=API_KEY)

# Liste des modèles par ordre de préférence (Point 3 : Fallback)
MODELES_DE_SECOURS = [
    'gemini-3-flash-preview',
    'gemini-3.1-flash-lite-preview',
    'gemini-2.5-flash',
    'gemini-2.5-flash-lite'
]

# ==========================================
# FONCTIONS UTILITAIRES & INTELLIGENCE
# ==========================================
def charger_tache_du_jour(fichier_backlog="backlog.json"):
    if not os.path.exists(fichier_backlog):
        return None, -1, []
    with open(fichier_backlog, "r", encoding="utf-8") as f:
        backlog = json.load(f)
    for i, tache in enumerate(backlog):
        if tache.get("status") == "pending":
            return tache, i, backlog
    return None, -1, backlog

def lire_contexte_cible(fichiers_contexte):
    contexte = ""
    for chemin in fichiers_contexte:
        if os.path.exists(chemin):
            with open(chemin, "r", encoding="utf-8") as f:
                contexte += f"\n--- Fichier : {chemin} ---\n{f.read()}\n"
    return contexte if contexte else "Aucun contexte fourni."

def verifier_syntaxe_python(code):
    """Vérifie la syntaxe Python. Retourne (True, "") ou (False, "message d'erreur")."""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        erreur = f"SyntaxError à la ligne {e.lineno} : {e.msg}"
        if e.text:
            erreur += f"\nCode fautif : {e.text.strip()}"
        return False, erreur
    except Exception as e:
        return False, f"Erreur d'analyse : {str(e)}"

def appliquer_patch(contenu_original, reponse_ia):
    """Applique de multiples patchs si les balises SEARCH/REPLACE sont présentes (Point 1)."""
    if "<<<SEARCH>>>" not in reponse_ia or "<<<REPLACE>>>" not in reponse_ia:
        return reponse_ia 

    nouveau_contenu = contenu_original
    # Utilisation de finditer pour trouver TOUS les blocs de patchs
    pattern = re.compile(r"<<<SEARCH>>>(.*?)<<<REPLACE>>>(.*?)(?:<<<END>>>|$)", re.DOTALL)
    matches = list(pattern.finditer(reponse_ia))

    if not matches:
        print("⚠️ [PATCH] Balises présentes mais mal formatées. Remplacement complet appliqué.")
        return reponse_ia

    patch_reussis = 0
    for match in matches:
        search_block = match.group(1).strip()
        replace_block = match.group(2).strip()
        
        if search_block and search_block in nouveau_contenu:
            # On remplace l'occurrence exacte
            nouveau_contenu = nouveau_contenu.replace(search_block, replace_block, 1)
            patch_reussis += 1
        else:
            # Le bloc précis n'a pas été trouvé
            snippet = search_block[:40].replace('\n', ' ') + "..." if search_block else "Bloc vide"
            print(f"⚠️ [PATCH] Un bloc SEARCH n'a pas été trouvé dans le code original (Ignoré) : {snippet}")
            
    if patch_reussis > 0:
        print(f"🔧 [PATCH] {patch_reussis} modification(s) chirurgicale(s) appliquée(s) avec succès !")
        return nouveau_contenu
    else:
        print("⚠️ [PATCH] Aucun bloc SEARCH n'a correspondu. La réponse brute est renvoyée pour déclencher l'auto-correction.")
        return reponse_ia

# ==========================================
# MOTEUR DE GÉNÉRATION (Avec Boucles Séparées)
# ==========================================
def generer_code_ia(contexte, description_tache, role, fichier_cible):
    contenu_existant = ""
    mode_patch = False
    if os.path.exists(fichier_cible):
        with open(fichier_cible, "r", encoding="utf-8") as f:
            contenu_existant = f.read()
            if contenu_existant.strip():
                mode_patch = True

    prompt_base = f"""Tu agis en tant que : {role}.
Tu travailles sur un Applicant Tracking System (ATS).
Contexte actuel : {contexte}
Ta mission : {description_tache}
Fichier cible : {fichier_cible}
"""

    if mode_patch:
        prompt_base += f"""
Le fichier existe déjà. Voici son contenu :

{contenu_existant}

CRITIQUE : Ne renvoie PAS tout le fichier. Renvoie UNIQUEMENT les modifications à l'aide de ces balises strictes.
Tu peux utiliser plusieurs blocs de recherche/remplacement si tu dois modifier plusieurs endroits différents du fichier.
Format exigé pour CHAQUE modification :
<<<SEARCH>>>
[copie ici exactement les quelques lignes existantes à remplacer]
<<<REPLACE>>>
[mets ici le nouveau code]
<<<END>>>
"""
    else:
        prompt_base += "\nCRITIQUE : Ne renvoie ABSOLUMENT RIEN d'autre que le code final. Pas de blabla, pas de balises markdown."

    max_tentatives_syntaxe = 3 
    prompt_actuel = prompt_base

    print(f"🧠 [IA] Requête initialisée (Mode Patch: {mode_patch})...")

    # Boucle Externe : Les vies pour l'Auto-Correction (Syntaxe Python)
    for tentative_syntaxe in range(max_tentatives_syntaxe):
        reponse_brute = None
        
        # Boucle Interne : Les vies pour le Réseau et l'API (Point 2)
        for nom_modele in MODELES_DE_SECOURS:
            try:
                print(f"📡 Appel API avec {nom_modele} (Tentative syntaxe {tentative_syntaxe+1}/{max_tentatives_syntaxe})...")
                response = client.models.generate_content(
                    model=nom_modele,
                    contents=prompt_actuel
                )
                reponse_brute = response.text.strip()
                print(f"✅ [API] Réponse obtenue de {nom_modele} !")
                break # Succès API : on sort de la boucle des modèles
            except Exception as e:
                print(f"⚠️ [API] Erreur réseau/serveur avec {nom_modele} : {e}")
                print("⏳ Pause de 5 secondes avant d'essayer le modèle suivant...")
                time.sleep(5)
                continue # On passe au modèle de secours suivant
                
        # Si la boucle interne finit sans aucune réponse
        if not reponse_brute:
            print("❌ [API] Tous les modèles de secours ont échoué. Arrêt du script.")
            return None

        # Nettoyage Markdown
        code = re.sub(r"^```[a-zA-Z]*\s*", "", reponse_brute, flags=re.IGNORECASE)
        code = re.sub(r"\s*```$", "", code)
        
        # Application des Patchs (s'il y en a)
        if mode_patch:
            code_final = appliquer_patch(contenu_existant, code)
        else:
            code_final = code.strip()

        # Vérification de la Syntaxe Python
        if fichier_cible.endswith(".py"):
            est_valide, erreur_msg = verifier_syntaxe_python(code_final)
            if not est_valide:
                print(f"🐛 [AST] Erreur de syntaxe détectée : {erreur_msg}")
                if tentative_syntaxe < max_tentatives_syntaxe - 1:
                    print("🔄 Renvoi de la copie à l'IA pour auto-correction...")
                    prompt_actuel += f"\n\nTON DERNIER CODE A ÉCHOUÉ AVEC CETTE ERREUR :\n{erreur_msg}\nS'il te plaît, corrige l'erreur de syntaxe. Si tu as fait une erreur dans les balises SEARCH, assure-toi de copier EXACTEMENT le texte d'origine."
                    continue # On utilise une "vie" de syntaxe
                else:
                    print("❌ [AST] L'IA n'a pas réussi à corriger le code après 3 essais.")
                    return None
        
        return code_final
        
    return None

# ==========================================
# EXÉCUTION GIT
# ==========================================
def executer_git(fichier_cible, description_tache):
    desc_propre = description_tache.replace('\n', ' ')
    commit_msg = f"feat: {desc_propre[:45]}..."
    print("\n[GIT] Vérification des modifications...")
    try:
        subprocess.run(["git", "config", "--local", "user.name", "AchrafAmeri"], check=True)
        subprocess.run(["git", "config", "--local", "user.email", "ameriachraftoulouse@gmail.com"], check=True)
        subprocess.run(["git", "add", fichier_cible], check=True)
        subprocess.run(["git", "add", "backlog.json"], check=True)
        
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status.stdout.strip():
            print("ℹ️ [GIT] Aucun changement détecté. Pas de commit.")
            return

        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        print(f"✅ [GIT] Commit validé : '{commit_msg}'")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ [GIT] Erreur Git : {e}")

# ==========================================
# EXÉCUTION PRINCIPALE
# ==========================================
if __name__ == "__main__":
    tache, index, backlog = charger_tache_du_jour()
    
    if not tache:
        print("🎉 Projet terminé !")
        exit(0)
        
    print("="*50)
    print(f"🚀 JOUR {tache.get('jour', '?')} | Rôle : {tache.get('role', 'Dev')}")
    print(f"📁 Cible : {tache['fichier_cible']}")
    print("="*50)
    
    contexte = lire_contexte_cible(tache.get('fichiers_contexte', []))
    nouveau_code = generer_code_ia(contexte, tache['description'], tache.get('role', 'Dev'), tache['fichier_cible'])
    
    if nouveau_code:
        dossier = os.path.dirname(tache['fichier_cible'])
        if dossier: os.makedirs(dossier, exist_ok=True)
            
        with open(tache['fichier_cible'], "w", encoding="utf-8") as f:
            f.write(nouveau_code)
        
        print(f"✅ Fichier '{tache['fichier_cible']}' sauvegardé.")
        
        backlog[index]["status"] = "done"
        with open("backlog.json", "w", encoding="utf-8") as f:
            json.dump(backlog, f, indent=4, ensure_ascii=False)
            
        executer_git(tache['fichier_cible'], tache['description'])
    else:
        print("❌ Échec de la tâche.")