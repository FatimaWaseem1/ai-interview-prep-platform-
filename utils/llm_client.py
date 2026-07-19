"""
Thin wrapper so every module calls one function - get_llm_response() -
regardless of which provider is configured in .env. Keeps prompt
modules provider-agnostic and makes swapping Gemini <-> OpenAI trivial.
"""
import json
from config import settings


def _call_gemini(system_prompt: str, user_prompt: str, json_mode: bool) -> str:
    import google.generativeai as genai

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(
        settings.GEMINI_MODEL,
        system_instruction=system_prompt,
    )
    generation_config = {"response_mime_type": "application/json"} if json_mode else {}
    response = model.generate_content(user_prompt, generation_config=generation_config)
    return response.text


def _call_openai(system_prompt: str, user_prompt: str, json_mode: bool) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    completion = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **kwargs,
    )
    return completion.choices[0].message.content


def get_llm_response(system_prompt: str, user_prompt: str, json_mode: bool = False):
    """
    Single entry point for every LLM call in the app.

    Args:
        system_prompt: role/context/instructions for the model.
        user_prompt: the actual task/content for this call.
        json_mode: if True, asks the provider for structured JSON output
                    and parses it into a dict before returning.

    Returns:
        str if json_mode is False, otherwise a parsed dict/list.
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "gemini":
        raw = _call_gemini(system_prompt, user_prompt, json_mode)
    elif provider == "openai":
        raw = _call_openai(system_prompt, user_prompt, json_mode)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")

    if json_mode:
        # Strip accidental markdown code fences before parsing.
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)

    return raw