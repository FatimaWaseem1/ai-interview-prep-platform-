"""
Main entry point. Run with: streamlit run app.py

This file only handles: page config, DB init, session-state bootstrap,
and a landing/welcome screen. The actual features live in pages/ as a
Streamlit multipage app (each file in pages/ shows up as a sidebar tab).
"""
import streamlit as st
from config import settings
from database.db import init_db

st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="🧠",
    layout="wide",
)

init_db()

# --- Bootstrap shared session state ---
defaults = {
    "user_id": None,
    "user_name": None,
    "resume_id": None,
    "resume_profile": None,
    "job_role": None,
    "experience_level": None,
    "current_session_id": None,
    "qa_records": [],          # running list during an active interview
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("🧠 AI Interview Preparation Platform")
st.write(
    """
    Welcome! Use the sidebar to:

    1. **Onboarding** — create your profile and upload your resume
    2. **Resume Analysis** — see your skill match, gaps, and ATS score
    3. **Technical Interview** — adaptive AI-driven technical Q&A
    4. **HR Interview** — behavioral/STAR-based Q&A
    5. **Feedback & Report** — scores, strengths, weak areas, and a
       downloadable PDF report
    6. **Learning Roadmap** — a personalized study plan for your gaps
    7. **History** — track your progress across past sessions
    """
)

if not st.session_state.user_id:
    st.info("Head to the **Onboarding** page in the sidebar to get started.")
else:
    st.success(f"Welcome back, {st.session_state.user_name}!")