"""
AI Feedback & Scoring Engine.

Takes the raw per-question scores stored during the interview and:
1. Computes deterministic aggregates (overall %, grade, per-section avg)
   in plain Python — no need to ask the LLM to do arithmetic.
2. Calls the LLM once with the full summary to generate the
   qualitative parts (strengths, weak areas, narrative, radar chart,
   improvement priorities) — see prompts/feedback_prompts.py.
"""
from config import settings
from utils.llm_client import get_llm_response
from prompts.feedback_prompts import build_narrative_feedback_prompt


def score_to_grade(percentage: float) -> str:
    for threshold, grade in settings.GRADE_BANDS:
        if percentage >= threshold:
            return grade
    return "F"


def compute_aggregate_scores(qa_records: list[dict]) -> dict:
    """
    qa_records: list of {"category": str, "mode": "Technical"|"HR",
                          "score": float (0-10)}
    Returns overall_score (0-100), grade, technical_score, hr_score.
    """
    if not qa_records:
        return {"overall_score": 0, "grade": "F", "technical_score": 0, "hr_score": 0}

    def avg(records):
        scores = [r["score"] for r in records]
        return round(sum(scores) / len(scores) * 10, 1) if scores else 0  # scale 0-10 -> 0-100

    technical_records = [r for r in qa_records if r["mode"] == "Technical"]
    hr_records = [r for r in qa_records if r["mode"] == "HR"]

    overall_score = avg(qa_records)

    return {
        "overall_score": overall_score,
        "grade": score_to_grade(overall_score),
        "technical_score": avg(technical_records),
        "hr_score": avg(hr_records),
    }


def generate_qualitative_feedback(qa_summary: list[dict], job_role: str) -> dict:
    """
    qa_summary: list of {"category", "question", "score", "rationale"}
    Returns strengths, weak_areas, skill_radar, narrative_feedback,
    improvement_priority_list — see prompts/feedback_prompts.py schema.
    """
    system_prompt, user_prompt = build_narrative_feedback_prompt(qa_summary, job_role)
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def build_full_scoring_report(qa_records: list[dict], job_role: str) -> dict:
    """Orchestrator: combine deterministic + LLM-generated feedback."""
    aggregates = compute_aggregate_scores(qa_records)
    qualitative = generate_qualitative_feedback(qa_records, job_role)
    return {**aggregates, **qualitative}