"""
AI HR Interview Module (STAR-based behavioral questions).
Mirrors the technical module's structure for consistency.
"""
from utils.llm_client import get_llm_response
from prompts.hr_prompts import build_hr_question_prompt, build_hr_evaluation_prompt


def generate_hr_question(resume_profile: dict, category: str) -> dict:
    system_prompt, user_prompt = build_hr_question_prompt(resume_profile, category)
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def evaluate_hr_answer(question: str, candidate_answer: str) -> dict:
    system_prompt, user_prompt = build_hr_evaluation_prompt(question, candidate_answer)
    return get_llm_response(system_prompt, user_prompt, json_mode=True)