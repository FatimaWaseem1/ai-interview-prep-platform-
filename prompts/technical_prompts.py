"""
Prompt templates for the AI Technical Interview module.
"""

TECHNICAL_INTERVIEWER_SYSTEM = """You are a rigorous but fair senior
technical interviewer at a top tech company. You ask questions calibrated
to the candidate's stated experience level and resume. You never reveal
the answer inside the question itself."""


def build_question_prompt(resume_profile: dict, job_role: str, difficulty: str,
                           category: str, previous_performance: str = "") -> tuple[str, str]:
    """
    Generate one adaptive technical question.
    previous_performance: short note like "candidate struggled with Big-O
    analysis on the last question" to drive adaptive difficulty / follow-ups.
    """
    user_prompt = f"""
Candidate resume profile (JSON): {resume_profile}
Target role: {job_role}
Difficulty level: {difficulty}
Question category: {category}
Notes on previous performance (may be empty): {previous_performance}

Generate ONE interview question for this category, calibrated to the
difficulty level and grounded in the candidate's actual listed skills
when the category is "Technology-specific".

Return JSON:
{{
  "question": "...",
  "category": "{category}",
  "expects_code": true/false,
  "ideal_answer_points": ["key concept 1", "key concept 2", "..."]
}}
"""
    return TECHNICAL_INTERVIEWER_SYSTEM, user_prompt


def build_answer_evaluation_prompt(question: str, ideal_answer_points: list,
                                    candidate_answer: str) -> tuple[str, str]:
    """Score a candidate's answer to a technical question."""
    system_prompt = """You are grading a technical interview answer.
Be objective and consistent. Partial credit is allowed when the
candidate demonstrates correct reasoning even with an incomplete
answer."""

    user_prompt = f"""
Question: {question}
Key concepts expected: {ideal_answer_points}
Candidate's answer: \"\"\"{candidate_answer}\"\"\"

Return JSON:
{{
  "score": 0-10,
  "rationale": "2-3 sentences explaining the score, referencing which
                 key concepts were covered or missed",
  "needs_followup": true/false,
  "followup_question": "only if needs_followup is true, else empty string"
}}
"""
    return system_prompt, user_prompt