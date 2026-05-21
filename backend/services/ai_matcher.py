import os
from google import genai
from backend.config import settings
from backend.models import AnalysisResult

# Initialisation du client Gemini
client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())

async def analyze_cv_vs_job(cv_text: str, job_description: str) -> AnalysisResult:
    """
    Analyse la correspondance entre un CV et une offre d'emploi.
    Note : Version mockée pour la mise en place de la structure.
    """
    return AnalysisResult(
        score=75,
        points_forts=[
            "Expérience professionnelle en adéquation avec le poste",
            "Compétences techniques clés identifiées",
            "Structure du CV claire et lisible"
        ],
        points_amelioration=[
            "Manque de certifications spécifiques mentionnées dans l'offre",
            "Absence de certains mots-clés secondaires",
            "Les réalisations chiffrées pourraient être plus détaillées"
        ]
    )