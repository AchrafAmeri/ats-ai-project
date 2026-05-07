from pydantic import BaseModel

class JobOffer(BaseModel):
    title: str
    description: str

class AnalysisResult(BaseModel):
    score: int
    points_forts: list[str]
    points_amelioration: list[str]