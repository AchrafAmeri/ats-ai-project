from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class JobOffer(BaseModel):
    title: str
    description: str

class AnalysisResult(BaseModel):
    score: int
    points_forts: list[str]
    points_amelioration: list[str]