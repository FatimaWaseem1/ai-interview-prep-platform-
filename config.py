"""
Central configuration for the AI Interview Preparation Platform.
Loads environment variables once and exposes typed settings used
across modules, pages, and the RAG pipeline.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- LLM provider ---
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" | "openai"

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # --- Storage ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///data/app.db")
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "data/chroma")

    # --- App-level constants ---
    APP_NAME = "AI Interview Preparation Platform"

    JOB_ROLES = [
        "Software Engineer (Backend)",
        "Software Engineer (Frontend)",
        "Full Stack Developer",
        "Data Scientist",
        "Data Analyst",
        "ML Engineer",
        "DevOps Engineer",
        "Mobile Developer (Flutter/React Native)",
        "Product Manager",
        "Other (custom)",
    ]

    EXPERIENCE_LEVELS = ["Junior", "Mid-level", "Senior"]
    INTERVIEW_MODES = ["Technical", "HR", "Full Mock Interview"]

    TECHNICAL_CATEGORIES = [
        "Data Structures",
        "Algorithms",
        "System Design",
        "Technology-specific",
        "Problem Solving",
    ]

    HR_CATEGORIES = [
        "Motivation",
        "Teamwork",
        "Conflict Resolution",
        "Leadership",
        "Communication",
        "Career Goals",
    ]

    GRADE_BANDS = [
        (90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F"),
    ]

    QUESTION_TIMER_SECONDS = 120


settings = Settings()