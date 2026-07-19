"""
Resume Analysis Module.

Pipeline:
1. Index the raw resume text into ChromaDB (per-user collection).
2. Ask the LLM to extract a structured profile (skills/experience/etc.).
3. Ask the LLM to compute skill gaps vs. the target role / JD.
4. Ask the LLM to score resume quality + ATS compatibility.

Each step is a separate, focused LLM call (see prompts/resume_prompts.py)
rather than one giant prompt — this keeps outputs more reliable and
easier to debug/tune independently.
"""
from rag.vector_store import index_document, retrieve_relevant_chunks
from utils.llm_client import get_llm_response
from prompts.resume_prompts import (
    build_resume_profile_prompt,
    build_skill_gap_prompt,
    build_resume_quality_prompt,
)


def index_resume(user_id: int, resume_text: str):
    """Chunk + embed the resume so later steps (and interview question
    generation) can retrieve relevant snippets instead of re-sending
    the full resume text every time."""
    index_document(
        collection_name=f"resume_{user_id}",
        text=resume_text,
        metadata={"type": "resume", "user_id": user_id},
    )


def extract_resume_profile(resume_text: str) -> dict:
    system_prompt, user_prompt = build_resume_profile_prompt(resume_text)
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def analyze_skill_gap(resume_profile: dict, job_role: str, job_description: str = "") -> dict:
    system_prompt, user_prompt = build_skill_gap_prompt(resume_profile, job_role, job_description)
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def analyze_resume_quality(resume_text: str, job_role: str) -> dict:
    system_prompt, user_prompt = build_resume_quality_prompt(resume_text, job_role)
    return get_llm_response(system_prompt, user_prompt, json_mode=True)


def run_full_resume_analysis(user_id: int, resume_text: str, job_role: str,
                              job_description: str = "") -> dict:
    """
    Convenience orchestrator used by the Streamlit page. Runs the full
    pipeline and returns one combined dict ready to render + persist.
    """
    index_resume(user_id, resume_text)

    profile = extract_resume_profile(resume_text)
    gap_analysis = analyze_skill_gap(profile, job_role, job_description)
    quality_analysis = analyze_resume_quality(resume_text, job_role)

    return {
        "profile": profile,
        "gap_analysis": gap_analysis,
        "quality_analysis": quality_analysis,
    }


def get_relevant_resume_context(user_id: int, query: str, k: int = 4) -> list[str]:
    """Used by interview modules to pull only the relevant resume
    snippets for a given question topic (RAG retrieval step)."""
    return retrieve_relevant_chunks(f"resume_{user_id}", query, k=k)