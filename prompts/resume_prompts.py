"""
Prompt templates for the Resume Analysis module.
Each function returns (system_prompt, user_prompt) ready to pass to
utils.llm_client.get_llm_response().
"""

RESUME_PROFILE_SYSTEM = """You are an expert technical recruiter and resume
analyst. You extract structured, factual information from resumes only —
never invent skills, employers, or dates that are not present in the text.
Always respond with valid JSON matching exactly the schema requested."""


def build_resume_profile_prompt(resume_text: str) -> tuple[str, str]:
    """Extract structured profile: skills, experience, education, projects."""
    user_prompt = f"""
Extract a structured profile from the resume text below.

Resume text:
\"\"\"{resume_text}\"\"\"

Return JSON with exactly this schema:
{{
  "skills": ["..."],
  "experience": [{{"role": "...", "company": "...", "duration": "...", "highlights": ["..."]}}],
  "education": [{{"degree": "...", "institution": "...", "year": "..."}}],
  "projects": [{{"name": "...", "description": "...", "technologies": ["..."]}}],
  "certifications": ["..."]
}}
"""
    return RESUME_PROFILE_SYSTEM, user_prompt


def build_skill_gap_prompt(resume_profile: dict, job_role: str, job_description: str = "") -> tuple[str, str]:
    """Compare candidate skills against the target role / JD."""
    system_prompt = """You are a senior technical hiring manager. Compare a
candidate's profile against a target role objectively. Be specific and
avoid generic filler like "good communication skills" unless evidenced."""

    user_prompt = f"""
Candidate profile (JSON): {resume_profile}

Target job role: {job_role}
Job description (optional, may be empty): {job_description}

Return JSON:
{{
  "matched_skills": ["..."],
  "missing_skills": ["..."],
  "qualification_gaps": ["..."],
  "match_percentage": 0-100
}}
"""
    return system_prompt, user_prompt


def build_resume_quality_prompt(resume_text: str, job_role: str) -> tuple[str, str]:
    """Score resume quality + ATS compatibility + actionable suggestions."""
    system_prompt = """You are an expert resume reviewer and ATS
(Applicant Tracking System) specialist. Give direct, actionable, and
encouraging feedback. Never be vague."""

    user_prompt = f"""
Resume text:
\"\"\"{resume_text}\"\"\"

Target role: {job_role}

Return JSON:
{{
  "resume_score": 0-100,
  "section_scores": {{"Summary": 0-100, "Experience": 0-100, "Skills": 0-100,
                        "Education": 0-100, "Projects": 0-100}},
  "ats_score": 0-100,
  "ats_checklist": [{{"item": "...", "pass": true}}],
  "quality_feedback": "2-3 sentence overview of clarity/completeness/formatting",
  "bullet_point_suggestions": [
    {{"section": "Experience", "original": "...", "improved": "..."}}
  ]
}}
"""
    return system_prompt, user_prompt