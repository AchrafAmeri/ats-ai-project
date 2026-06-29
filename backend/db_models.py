from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class AnalysisRecord(Base):
    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    candidate_name = Column(String, nullable=True)
    score = Column(Integer)
    points_forts = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))