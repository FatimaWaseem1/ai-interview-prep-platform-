"""
Prompt templates for the AI HR Interview module (STAR-framework based).
"""

HR_INTERVIEWER_SYSTEM = """You are an experienced HR interviewer. You ask
behavioral and situational questions using the STAR framework (Situation,
Task, Action, Result). Where possible you reference specifics from the
candidate's resume to make questions feel personalized and relevant."""


def build_hr_question_prompt(resume_profile: dict, category: str) -> tuple[str, str]:
    user_prompt = f"""
Candidate resume profile (JSON): {resume_profile}
Question category: {category}

Generate ONE behavioral/situational HR question in this category. If the
resume contains a specific past role, project, or achievement relevant to
this category, reference it directly in the question.

Return JSON:
{{
  "question": "...",
  "category": "{category}",
  "star_focus": ["Situation", "Task", "Action", "Result"]
}}
"""
    return HR_INTERVIEWER_SYSTEM, user_prompt


def build_hr_evaluation_prompt(question: str, candidate_answer: str) -> tuple[str, str]:
    system_prompt = """You are evaluating an HR interview answer for
professionalism, clarity, STAR structure, and relevance. You also assess
tone/sentiment and overall confidence conveyed in the writing."""

    user_prompt = f"""
Question: {question}
Candidate's answer: \"\"\"{candidate_answer}\"\"\"

Return JSON:
{{
  "score": 0-10,
  "star_coverage": {{"situation": true, "task": true, "action": true, "result": false}},
  "tone_sentiment": "confident | neutral | uncertain | negative",
  "rationale": "2-3 sentences",
  "needs_followup": true/false,
  "followup_question": "only if needs_followup is true, else empty string",
  "ideal_model_answer": "a strong example answer to this question, 3-4 sentences"
}}
"""
    return system_prompt, user_prompt