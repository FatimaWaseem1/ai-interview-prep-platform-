"""
HR Interview page. Mirrors the Technical Interview page's loop but
uses STAR-based behavioral questions and different evaluation criteria.
"""
import streamlit as st
from config import settings
from modules.interview_hr import generate_hr_question, evaluate_hr_answer

st.header("🗣️ HR Interview")

if not st.session_state.get("resume_profile"):
    st.warning("Please run Resume Analysis first so questions can be personalized.")
    st.stop()

if "current_hr_question" not in st.session_state:
    st.session_state.current_hr_question = None

category = st.selectbox("Question category", settings.HR_CATEGORIES)

if st.button("Get Next Question"):
    with st.spinner("Generating question..."):
        st.session_state.current_hr_question = generate_hr_question(
            resume_profile=st.session_state.resume_profile,
            category=category,
        )

q = st.session_state.current_hr_question
if q:
    st.subheader(f"[{q['category']}] {q['question']}")
    answer = st.text_area("Your answer (try to use the STAR structure)", height=180)

    if st.button("Submit Answer"):
        with st.spinner("Evaluating..."):
            evaluation = evaluate_hr_answer(question=q["question"], candidate_answer=answer)

        st.metric("Score", f"{evaluation['score']}/10")
        st.write(f"**Tone:** {evaluation['tone_sentiment']}")
        st.write(evaluation["rationale"])

        with st.expander("See ideal model answer"):
            st.write(evaluation["ideal_model_answer"])

        st.session_state.qa_records.append({
            "mode": "HR",
            "category": q["category"],
            "question": q["question"],
            "answer": answer,
            "score": evaluation["score"],
            "rationale": evaluation["rationale"],
        })

        if evaluation.get("needs_followup"):
            st.info(f"Follow-up: {evaluation['followup_question']}")

st.caption(f"Questions answered this session: {len(st.session_state.qa_records)}")