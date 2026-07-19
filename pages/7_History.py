"""
Interview History & Progress Tracking page.

TODO: This currently reads directly from InterviewSession rows. Wire
up the Feedback & Report page to actually create/complete an
InterviewSession row (currently it only uses in-memory session_state)
so history has real data to show across visits.
"""
import streamlit as st
import pandas as pd
from database.db import SessionLocal
from database.models import InterviewSession

st.header("📈 Interview History & Progress")

if not st.session_state.get("user_id"):
    st.warning("Please complete Onboarding first.")
    st.stop()

db = SessionLocal()
try:
    sessions = (
        db.query(InterviewSession)
        .filter_by(user_id=st.session_state.user_id)
        .order_by(InterviewSession.started_at)
        .all()
    )
finally:
    db.close()

if not sessions:
    st.info("No completed sessions yet. Once the report-saving TODO above "
             "is wired up, your past attempts will show here.")
else:
    df = pd.DataFrame([{
        "Date": s.started_at,
        "Role": s.job_role,
        "Mode": s.mode,
        "Overall Score": s.overall_score,
        "Grade": s.grade,
    } for s in sessions])

    st.dataframe(df, use_container_width=True)

    st.subheader("Score Trend")
    st.line_chart(df.set_index("Date")["Overall Score"])