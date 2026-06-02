from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ATS API is running"}

@patch("backend.routes.api.extract_text_from_pdf")
@patch("backend.routes.api.analyze_cv_vs_job")
def test_analyze_route(mock_analyze, mock_extract):
    # Mock des retours des services
    mock_extract.return_value = "Expérience en tests automatisés et Python."
    mock_analyze.return_value = {
        "score": 90,
        "summary": "Excellent candidat",
        "missing_skills": ["Docker"]
    }

    # Simulation du fichier PDF et de la description de poste
    file_data = {"file": ("resume.pdf", b"%PDF-1.4 fake content", "application/pdf")}
    payload = {"job_description": "Ingénieur QA avec expérience FastAPI"}

    # Exécution de la requête
    response = client.post("/api/v1/analyze", files=file_data, data=payload)

    # Assertions
    assert response.status_code == 200
    json_response = response.json()
    assert "score" in json_response
    assert json_response["score"] == 90
    mock_extract.assert_called_once()
    mock_analyze.assert_called_once()