"""
Resume Analysis page. Runs the full resume_analysis pipeline and
renders skills/gaps/quality/ATS results.
"""
import streamlit as st
from database.db import SessionLocal
from database.models import Resume
from modules.resume_analysis import run_full_resume_analysis

st.header("📄 Resume Analysis")

if not st.session_state.get("user_id"):
    st.warning("Please complete Onboarding first.")
    st.stop()

if st.button("Run Resume Analysis"):
    db = SessionLocal()
    try:
        resume = db.query(Resume).get(st.session_state.resume_id)
        with st.spinner("Analyzing resume with AI... this calls the LLM 3 times "
                         "(profile extraction, skill gap, quality/ATS scoring)."):
            results = run_full_resume_analysis(
                user_id=st.session_state.user_id,
                resume_text=resume.raw_text,
                job_role=st.session_state.job_role,
                job_description=st.session_state.get("job_description", ""),
            )

        # Persist scores back onto the resume row
        resume.parsed_profile = results["profile"]
        resume.resume_score = results["quality_analysis"].get("resume_score")
        resume.ats_score = results["quality_analysis"].get("ats_score")
        db.commit()

        st.session_state.resume_profile = results["profile"]
        st.session_state.resume_analysis_results = results
    finally:
        db.close()

results = st.session_state.get("resume_analysis_results")
if results:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resume Score", f"{results['quality_analysis'].get('resume_score', '-')}/100")
    with col2:
        st.metric("ATS Score", f"{results['quality_analysis'].get('ats_score', '-')}/100")

    st.subheader("Skill Gap Analysis")
    st.json(results["gap_analysis"])

    st.subheader("Resume Quality Feedback")
    st.write(results["quality_analysis"].get("quality_feedback", ""))

    st.subheader("Bullet-Point Suggestions")
    for suggestion in results["quality_analysis"].get("bullet_point_suggestions", []):
        st.markdown(f"**{suggestion.get('section')}**")
        st.markdown(f"- Original: {suggestion.get('original')}")
        st.markdown(f"- Improved: {suggestion.get('improved')}")

    st.subheader("Extracted Profile")
    st.json(results["profile"])
else:
    st.info("Click 'Run Resume Analysis' to get started.")