"""
AI Technical Interview Module.

Adaptive flow (driven from the Streamlit page):
1. generate_question() for the current category/difficulty.
2. Show question to candidate, start timer.
3. evaluate_answer() when they submit (or timer expires -> empty answer).
4. If needs_followup -> generate_question() using the followup text
   instead of a fresh category prompt.
5. Adjust `difficulty` for the next question based on the score
   (see adjust_difficulty()).
"""
from utils.llm_client import get_llm_response
from prompts.technical_prompts import (
    build_question_prompt,
    build_answer_evaluation_prompt,
)

DIFFICULTY_ORDER = ["Junior", "Mid-level", "Senior"]


def generate_question(resume_profile: dict, job_role: str, difficulty: str,
                       category: str, previous_performance: str = "") -> dict:
    system_prompt, user_prompt = build_question_prompt(
        resume_profile, job_role, difficulty, category, previous_performance
    )
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def evaluate_answer(question: str, ideal_answer_points: list, candidate_answer: str) -> dict:
    system_prompt, user_prompt = build_answer_evaluation_prompt(
        question, ideal_answer_points, candidate_answer
    )
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def adjust_difficulty(current_difficulty: str, last_score: float) -> str:
    """
    Simple adaptive rule:
    - score >= 8/10 -> step up a level (if not already Senior)
    - score <= 4/10 -> step down a level (if not already Junior)
    - otherwise stay the same
    """
    idx = DIFFICULTY_ORDER.index(current_difficulty)

    if last_score >= 8 and idx < len(DIFFICULTY_ORDER) - 1:
        idx += 1
    elif last_score <= 4 and idx > 0:
        idx -= 1

    return DIFFICULTY_ORDER[idx]