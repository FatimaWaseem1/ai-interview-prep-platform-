"""
Prompt templates for the Learning Roadmap Generator.
"""

ROADMAP_SYSTEM = """You are a career coach and curriculum designer. You
build realistic, prioritized learning roadmaps. You recommend genuinely
well-known, real resources (courses, docs, books, YouTube channels) —
never invent fake course names or URLs."""


def build_roadmap_prompt(weak_areas: list[str], job_role: str,
                          hours_per_week: int) -> tuple[str, str]:
    user_prompt = f"""
Target role: {job_role}
Identified weak areas: {weak_areas}
Available study time: {hours_per_week} hours/week

Build a personalized learning roadmap. Return JSON:
{{
  "roadmap": [
    {{
      "topic": "...",
      "priority": "Critical | Important | Nice-to-Have",
      "estimated_weeks_to_competency": 0,
      "resources": [{{"type": "course|book|doc|video", "name": "...", "note": "..."}}],
      "mini_project": "a small project idea to practice this topic"
    }}
  ],
  "weekly_plan": [
    {{"week": 1, "focus_topics": ["..."], "hours_allocated": {hours_per_week}}}
  ],
  "milestones": ["milestone 1 description", "milestone 2 description"]
}}
"""
    return ROADMAP_SYSTEM, user_prompt