import os
from google import genai
from backend.config import settings
from backend.models import AnalysisResult
from backend.utils.prompts import SYSTEM_PROMPT_MATCHING

# Initialisation du client Gemini
client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())

async def analyze_cv_vs_job(cv_text: str, job_description: str) -> str:
    """
    Analyse la correspondance entre un CV et une offre d'emploi via l'API Gemini.
    """
    prompt_data = f"CV DU CANDIDAT :\n{cv_text}\n\nOFFRE D'EMPLOI :\n{job_description}"

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_data,
        config={
            'system_instruction': SYSTEM_PROMPT_MATCHING
        }
    )

    return response.text