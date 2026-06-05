from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.database import Base

class AnalysisRecord(Base):
    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    candidate_name = Column(String, nullable=True)
    score = Column(Integer)
    points_forts = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)