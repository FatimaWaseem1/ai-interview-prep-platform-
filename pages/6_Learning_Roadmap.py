"""
Learning Roadmap page. Uses the weak_areas from the scoring report to
generate + display + export a personalized roadmap.
"""
import os
import streamlit as st
from modules.roadmap_generator import generate_roadmap, export_roadmap_pdf

st.header("🗺️ Learning Roadmap")

report = st.session_state.get("scoring_report")
if not report:
    st.warning("Generate your Feedback Report first (see Feedback & Report page).")
    st.stop()

hours_per_week = st.slider("Hours available per week for study", 1, 20, 5)

if st.button("Generate Roadmap"):
    with st.spinner("Building your personalized roadmap..."):
        roadmap = generate_roadmap(
            weak_areas=report.get("weak_areas", []),
            job_role=st.session_state.job_role,
            hours_per_week=hours_per_week,
        )
        st.session_state.roadmap = roadmap

roadmap = st.session_state.get("roadmap")
if roadmap:
    for item in roadmap.get("roadmap", []):
        with st.expander(f"[{item['priority']}] {item['topic']} (~{item['estimated_weeks_to_competency']} weeks)"):
            st.markdown("**Resources:**")
            for r in item.get("resources", []):
                st.markdown(f"- ({r['type']}) {r['name']} — {r.get('note', '')}")
            st.markdown(f"**Mini project:** {item.get('mini_project', '')}")

    st.subheader("Weekly Plan")
    st.table(roadmap.get("weekly_plan", []))

    st.subheader("Milestones")
    for m in roadmap.get("milestones", []):
        st.markdown(f"- {m}")

    if st.button("Export Roadmap PDF"):
        os.makedirs("data/reports", exist_ok=True)
        output_path = f"data/reports/roadmap_{st.session_state.user_id}.pdf"
        export_roadmap_pdf(roadmap, st.session_state.job_role, output_path)
        with open(output_path, "rb") as f:
            st.download_button("Download Roadmap PDF", f, file_name="learning_roadmap.pdf")