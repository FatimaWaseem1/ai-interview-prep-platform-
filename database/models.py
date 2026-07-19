"""
SQLAlchemy ORM models.

Tables:
- User: registered candidate profile
- Resume: uploaded resume + parsed profile JSON
- InterviewSession: one full interview attempt (technical/HR/mock)
- QuestionAnswer: each Q&A pair + score within a session
- LearningRoadmap: generated roadmap tied to a session
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    target_role = Column(String(120))
    experience_level = Column(String(50))
    industry = Column(String(120))
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user")
    sessions = relationship("InterviewSession", back_populates="user")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255))
    raw_text = Column(Text)
    parsed_profile = Column(JSON)          # skills, experience, education, projects
    resume_score = Column(Float)
    ats_score = Column(Float)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_role = Column(String(120))
    mode = Column(String(50))              # Technical | HR | Full Mock
    difficulty = Column(String(50))        # Junior | Mid-level | Senior
    status = Column(String(30), default="in_progress")  # in_progress | completed

    overall_score = Column(Float)
    grade = Column(String(2))
    technical_score = Column(Float)
    hr_score = Column(Float)

    strengths = Column(JSON)
    weak_areas = Column(JSON)
    skill_radar = Column(JSON)             # {"Communication": 7.5, ...}
    narrative_feedback = Column(Text)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="sessions")
    qa_pairs = relationship("QuestionAnswer", back_populates="session")
    roadmap = relationship("LearningRoadmap", back_populates="session", uselist=False)


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    category = Column(String(60))
    question_text = Column(Text)
    answer_text = Column(Text)
    score = Column(Float)
    rationale = Column(Text)
    is_followup = Column(Integer, default=0)  # 0/1 boolean
    time_taken_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="qa_pairs")


class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    roadmap_json = Column(JSON)      # structured: critical/important/nice-to-have
    weekly_plan = Column(JSON)
    generated_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="roadmap")