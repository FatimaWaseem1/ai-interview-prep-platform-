"""
Embedding function selection for the RAG pipeline. Keeps ChromaDB
provider-agnostic in the same way utils/llm_client.py does for chat.
"""
from config import settings


def get_embedding_function():
    """
    Returns a LangChain-compatible embedding function based on
    LLM_PROVIDER. Used when creating/querying the Chroma collection.
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "gemini":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=settings.GEMINI_API_KEY,
        )
    elif provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY,
        )
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}")