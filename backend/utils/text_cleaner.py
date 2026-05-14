import re

def clean_extracted_text(text: str) -> str:
    if not text:
        return ""

    # Supprime les caractères non imprimables (codes de contrôle ASCII)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    # Remplace les espaces horizontaux multiples (espaces, tabulations) par un seul espace
    text = re.sub(r'[ \t]+', ' ', text)

    # Remplace les sauts de ligne multiples par un seul
    text = re.sub(r'\n+', '\n', text)

    # Retire les espaces en début et fin de chaîne
    return text.strip()