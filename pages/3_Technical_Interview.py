"""
Technical Interview page. Adaptive question -> answer -> evaluate loop.

NOTE: this is a functional skeleton of the interaction loop. Wire in a
real timer (st.session_state + st_autorefresh or streamlit-extras'
timer component) for the "auto-submit on timeout" requirement, and
persist each QuestionAnswer row to the DB as you go (see
database/models.py::QuestionAnswer).
"""
import streamlit as st
from config import settings
from modules.interview_technical import generate_question, evaluate_answer, adjust_difficulty

st.header("💻 Technical Interview")

if not st.session_state.get("resume_profile"):
    st.warning("Please run Resume Analysis first so questions can be personalized.")
    st.stop()

if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "tech_difficulty" not in st.session_state:
    st.session_state.tech_difficulty = st.session_state.get("experience_level", "Junior")

category = st.selectbox("Question category", settings.TECHNICAL_CATEGORIES)

if st.button("Get Next Question"):
    with st.spinner("Generating question..."):
        st.session_state.current_question = generate_question(
            resume_profile=st.session_state.resume_profile,
            job_role=st.session_state.job_role,
            difficulty=st.session_state.tech_difficulty,
            category=category,
        )

q = st.session_state.current_question
if q:
    st.subheader(f"[{q['category']}] {q['question']}")
    if q.get("expects_code"):
        answer = st.text_area("Your answer (code + explanation)", height=200)
    else:
        answer = st.text_area("Your answer", height=150)

    if st.button("Submit Answer"):
        with st.spinner("Evaluating..."):
            evaluation = evaluate_answer(
                question=q["question"],
                ideal_answer_points=q.get("ideal_answer_points", []),
                candidate_answer=answer,
            )

        st.metric("Score", f"{evaluation['score']}/10")
        st.write(evaluation["rationale"])

        # Track for the scoring engine later
        st.session_state.qa_records.append({
            "mode": "Technical",
            "category": q["category"],
            "question": q["question"],
            "answer": answer,
            "score": evaluation["score"],
            "rationale": evaluation["rationale"],
        })

        # Adapt difficulty for next question
        st.session_state.tech_difficulty = adjust_difficulty(
            st.session_state.tech_difficulty, evaluation["score"]
        )

        if evaluation.get("needs_followup"):
            st.info(f"Follow-up: {evaluation['followup_question']}")

st.caption(f"Questions answered this session: {len(st.session_state.qa_records)}")