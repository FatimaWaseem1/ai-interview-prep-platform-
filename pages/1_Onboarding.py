"""
Onboarding page: registration/login (simplified), profile setup,
resume upload, and job role / JD input.

NOTE: auth here is intentionally minimal (name+email, no real password
hashing shown) to keep the scaffold focused on the AI features. Swap in
a real auth flow (e.g. streamlit-authenticator or a proper hashed
password check) before treating this as production-ready.
"""
import streamlit as st
from config import settings
from database.db import SessionLocal
from database.models import User, Resume
from modules.resume_parser import extract_resume_text
from modules.resume_analysis import index_resume

st.header("👤 Onboarding")

with st.form("profile_form"):
    name = st.text_input("Full name")
    email = st.text_input("Email")
    target_role = st.selectbox("Target job role", settings.JOB_ROLES)
    custom_role = st.text_input("If 'Other', specify role") if target_role == "Other (custom)" else ""
    experience_level = st.selectbox("Experience level", settings.EXPERIENCE_LEVELS)
    industry = st.text_input("Industry (e.g. FinTech, Healthcare, E-commerce)")

    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste job description (optional)", height=150)

    submitted = st.form_submit_button("Save & Continue")

if submitted:
    if not (name and email and resume_file):
        st.error("Name, email, and resume upload are required.")
    else:
        db = SessionLocal()
        try:
            # --- Upsert user (simplified: find-or-create by email) ---
            user = db.query(User).filter_by(email=email).first()
            if not user:
                user = User(
                    name=name, email=email, password_hash="placeholder",
                    target_role=custom_role or target_role,
                    experience_level=experience_level, industry=industry,
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            # --- Save resume file to disk, extract text ---
            save_path = f"data/uploads/{user.id}_{resume_file.name}"
            import os
            os.makedirs("data/uploads", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(resume_file.getbuffer())

            resume_text = extract_resume_text(save_path)

            resume = Resume(user_id=user.id, filename=resume_file.name, raw_text=resume_text)
            db.add(resume)
            db.commit()
            db.refresh(resume)

            # --- Index into vector store for RAG retrieval later ---
            index_resume(user.id, resume_text)

            # --- Populate session state for downstream pages ---
            st.session_state.user_id = user.id
            st.session_state.user_name = user.name
            st.session_state.resume_id = resume.id
            st.session_state.job_role = custom_role or target_role
            st.session_state.experience_level = experience_level
            st.session_state.job_description = job_description

            st.success("Profile saved! Head to **Resume Analysis** next.")
        finally:
            db.close()