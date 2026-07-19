"""
Prompt templates for the aggregate AI Feedback & Scoring Engine — the
module that turns a list of per-question scores into a holistic
narrative, strengths/weak-areas summary, and skill radar data.
"""

FEEDBACK_SYSTEM = """You are an encouraging but honest interview coach.
You synthesize per-question performance data into clear, specific,
motivating feedback. You never invent scores — you only summarize and
interpret the data given to you."""


def build_narrative_feedback_prompt(qa_summary: list[dict], job_role: str) -> tuple[str, str]:
    """
    qa_summary: list of {"category": str, "question": str, "score": float,
                          "rationale": str} across the whole session.
    """
    user_prompt = f"""
Job role: {job_role}
Per-question results: {qa_summary}

Based only on this data, return JSON:
{{
  "strengths": ["specific topic/skill the candidate did well on", "..."],
  "weak_areas": ["specific topic/skill that needs work", "..."],
  "skill_radar": {{"Communication": 0-10, "Problem Solving": 0-10,
                     "Technical Depth": 0-10, "Confidence": 0-10}},
  "narrative_feedback": "A warm, specific 4-6 sentence paragraph
                          summarizing overall performance.",
  "improvement_priority_list": ["top priority to fix", "2nd priority", "..."]
}}
"""
    return FEEDBACK_SYSTEM, user_prompt