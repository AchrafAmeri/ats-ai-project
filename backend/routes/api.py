import json
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.db_models import AnalysisRecord
from backend.services.pdf_extractor import extract_text_from_pdf
from backend.services.ai_matcher import analyze_cv_vs_job
from backend.utils.validators import validate_pdf_file
from backend.models import AnalysisResult

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validation du format du fichier (PDF)
    validate_pdf_file(file)
    
    # Lecture et extraction du texte
    file_bytes = await file.read()
    cv_text = await extract_text_from_pdf(file_bytes)
    
    # Appel du service AI pour l'analyse de correspondance
    result = await analyze_cv_vs_job(cv_text, job_description)
    
    # Sauvegarde de l'analyse en base de données
    db_record = AnalysisRecord(
        job_title=result.job_title,
        candidate_name=result.candidate_name,
        score=result.score,
        points_forts=json.dumps(result.points_forts)
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return result

@router.get("/history")
async def get_history(limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère l'historique des analyses effectuées, triées par date décroissante.
    """
    history = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit).all()
    return history