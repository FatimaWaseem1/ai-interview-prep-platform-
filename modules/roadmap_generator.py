"""
Learning Roadmap Generator Module.
Takes the weak-area list from the scoring engine and produces a
structured, prioritized roadmap + weekly study plan, then exports it
to PDF via utils/pdf_utils.py.
"""
from utils.llm_client import get_llm_response
from utils.pdf_utils import build_pdf
from prompts.roadmap_prompts import build_roadmap_prompt


def generate_roadmap(weak_areas: list[str], job_role: str, hours_per_week: int = 5) -> dict:
    system_prompt, user_prompt = build_roadmap_prompt(weak_areas, job_role, hours_per_week)
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def export_roadmap_pdf(roadmap: dict, job_role: str, output_path: str) -> str:
    """Renders the roadmap dict into a PDF file, returns the file path."""
    table_rows = [["Topic", "Priority", "Est. Weeks", "Mini Project"]]
    for item in roadmap.get("roadmap", []):
        table_rows.append([
            item.get("topic", ""),
            item.get("priority", ""),
            str(item.get("estimated_weeks_to_competency", "")),
            item.get("mini_project", ""),
        ])

    sections = [
        {
            "heading": "Roadmap Overview",
            "paragraphs": [f"Personalized learning roadmap for: {job_role}"],
        },
        {
            "heading": "Topics by Priority",
            "table": table_rows,
        },
        {
            "heading": "Milestones",
            "paragraphs": roadmap.get("milestones", []),
        },
    ]

    return build_pdf(output_path, "Personalized Learning Roadmap", sections)