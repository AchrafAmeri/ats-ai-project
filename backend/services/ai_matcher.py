import os
import re
import json
import logging
from google import genai
from backend.config import settings
from backend.models import AnalysisResult
from backend.utils.prompts import SYSTEM_PROMPT_MATCHING

# Initialisation du client Gemini
client = genai.Client(api_key=settings.GEMINI_API_KEY.get_secret_value())

async def analyze_cv_vs_job(cv_text: str, job_description: str) -> AnalysisResult:
    """
    Analyse la correspondance entre un CV et une offre d'emploi via l'API Gemini.
    """
    prompt_data = f"CV DU CANDIDAT :\n{cv_text}\n\nOFFRE D'EMPLOI :\n{job_description}"

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_data,
            config={
                'system_instruction': SYSTEM_PROMPT_MATCHING
            }
        )

        text = response.text
        # Supprime les balises markdown (ex: ```json ... ```) pour ne garder que le contenu JSON
        cleaned_json = re.sub(r'^```json\s*|\s*```$', '', text, flags=re.MULTILINE | re.DOTALL).strip()

        data = json.loads(cleaned_json)
        return AnalysisResult(**data)

    except (json.JSONDecodeError, Exception) as e:
        logging.error(f"Erreur lors de l'analyse AI (Gemini) : {str(e)}")
        # Retour d'un résultat par défaut en cas d'échec de l'API ou du parsing
        return AnalysisResult(
            score=0,
            strengths=[],
            improvements=[f"Erreur technique lors de l'analyse : {str(e)}"],
            conclusion="L'analyse automatique est temporairement indisponible."
        )