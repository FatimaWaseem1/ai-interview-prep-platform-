"""
Feedback & Scoring + Report Export page.
Aggregates st.session_state.qa_records into a full scoring report,
displays it, and lets the user download a PDF.
"""
import os
import streamlit as st
from modules.scoring_engine import build_full_scoring_report
from modules.report_generator import build_session_report

st.header("📊 Feedback & Report")

qa_records = st.session_state.get("qa_records", [])

if not qa_records:
    st.warning("No interview answers recorded yet. Complete some questions "
               "in the Technical or HR Interview pages first.")
    st.stop()

if st.button("Generate Feedback Report"):
    with st.spinner("Scoring session and generating feedback..."):
        report = build_full_scoring_report(qa_records, st.session_state.job_role)
        st.session_state.scoring_report = report

report = st.session_state.get("scoring_report")
if report:
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{report['overall_score']}%", report["grade"])
    col2.metric("Technical", f"{report['technical_score']}%")
    col3.metric("HR", f"{report['hr_score']}%")

    st.subheader("Skill Radar")
    st.json(report.get("skill_radar", {}))  # TODO: render as plotly radar chart

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("✅ Strengths")
        for s in report.get("strengths", []):
            st.markdown(f"- {s}")
    with col_b:
        st.subheader("⚠️ Weak Areas")
        for w in report.get("weak_areas", []):
            st.markdown(f"- {w}")

    st.subheader("Narrative Feedback")
    st.write(report.get("narrative_feedback", ""))

    st.subheader("Top Improvement Priorities")
    for p in report.get("improvement_priority_list", []):
        st.markdown(f"- {p}")

    if st.button("Export PDF Report"):
        os.makedirs("data/reports", exist_ok=True)
        output_path = f"data/reports/session_{st.session_state.user_id}.pdf"
        build_session_report(
            session_data={
                "candidate_name": st.session_state.user_name,
                "job_role": st.session_state.job_role,
                "resume_score": st.session_state.get("resume_analysis_results", {})
                    .get("quality_analysis", {}).get("resume_score"),
                "overall_score": report["overall_score"],
                "grade": report["grade"],
                "technical_score": report["technical_score"],
                "hr_score": report["hr_score"],
                "qa_records": qa_records,
                "strengths": report.get("strengths", []),
                "weak_areas": report.get("weak_areas", []),
                "narrative_feedback": report.get("narrative_feedback", ""),
            },
            output_path=output_path,
        )
        with open(output_path, "rb") as f:
            st.download_button("Download PDF Report", f, file_name="interview_report.pdf")