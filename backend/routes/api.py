from fastapi import APIRouter, UploadFile, File, Form
from backend.services.pdf_extractor import extract_text_from_pdf
from backend.services.ai_matcher import analyze_cv_vs_job
from backend.models import AnalysisResult

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    file_bytes = await file.read()
    cv_text = await extract_text_from_pdf(file_bytes)
    result = await analyze_cv_vs_job(cv_text, job_description)
    return result