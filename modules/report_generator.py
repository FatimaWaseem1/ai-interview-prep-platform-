"""
Report Generation & Export Module.
Combines resume analysis + interview results + scoring + roadmap into
one exportable PDF performance report for a completed session.
"""
from utils.pdf_utils import build_pdf


def build_session_report(session_data: dict, output_path: str) -> str:
    """
    session_data expected keys:
        candidate_name, job_role, resume_score, overall_score, grade,
        technical_score, hr_score, qa_records (list of dict),
        strengths (list), weak_areas (list), narrative_feedback (str),
        roadmap (dict, optional)
    """
    qa_table = [["Category", "Question", "Score", "Rationale"]]
    for qa in session_data.get("qa_records", []):
        qa_table.append([
            qa.get("category", ""),
            (qa.get("question", "")[:80] + "...") if len(qa.get("question", "")) > 80 else qa.get("question", ""),
            str(qa.get("score", "")),
            (qa.get("rationale", "")[:100] + "...") if len(qa.get("rationale", "")) > 100 else qa.get("rationale", ""),
        ])

    sections = [
        {
            "heading": "Candidate Summary",
            "paragraphs": [
                f"Candidate: {session_data.get('candidate_name', 'N/A')}",
                f"Target Role: {session_data.get('job_role', 'N/A')}",
                f"Resume Score: {session_data.get('resume_score', 'N/A')}/100",
            ],
        },
        {
            "heading": "Interview Scores",
            "paragraphs": [
                f"Overall Score: {session_data.get('overall_score', 'N/A')}% "
                f"(Grade {session_data.get('grade', 'N/A')})",
                f"Technical Score: {session_data.get('technical_score', 'N/A')}%",
                f"HR Score: {session_data.get('hr_score', 'N/A')}%",
            ],
        },
        {
            "heading": "Per-Question Breakdown",
            "table": qa_table,
        },
        {
            "heading": "Strengths",
            "paragraphs": session_data.get("strengths", []),
        },
        {
            "heading": "Weak Areas",
            "paragraphs": session_data.get("weak_areas", []),
        },
        {
            "heading": "Narrative Feedback",
            "paragraphs": [session_data.get("narrative_feedback", "")],
        },
    ]

    if session_data.get("roadmap"):
        roadmap_topics = [item["topic"] for item in session_data["roadmap"].get("roadmap", [])]
        sections.append({
            "heading": "Recommended Learning Roadmap (Summary)",
            "paragraphs": [", ".join(roadmap_topics)] if roadmap_topics else ["See separate roadmap export."],
        })

    return build_pdf(output_path, "AI Interview Performance Report", sections)