"""
Vector store wrapper around ChromaDB. Stores resume + job description
chunks per user/session so resume_analysis.py and the interview
modules can retrieve relevant context instead of stuffing the full
resume into every prompt.

Collection naming convention: "resume_{user_id}" and "jd_{session_id}"
so retrieval stays scoped to the right candidate/session.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from config import settings
from rag.embeddings import get_embedding_function

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


def _get_store(collection_name: str) -> Chroma:
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embedding_function(),
        persist_directory=settings.CHROMA_PERSIST_DIR,
    )


def index_document(collection_name: str, text: str, metadata: dict | None = None):
    """
    Chunk + embed a document (resume or JD) and store it under
    collection_name. Call this once per upload.
    """
    chunks = _splitter.split_text(text)
    store = _get_store(collection_name)
    metadatas = [metadata or {} for _ in chunks]
    store.add_texts(texts=chunks, metadatas=metadatas)
    store.persist()


def retrieve_relevant_chunks(collection_name: str, query: str, k: int = 4) -> list[str]:
    """
    Semantic search within a collection. Used to pull the most
    relevant resume/JD snippets for a given prompt (e.g. "React
    experience" when generating a React question).
    """
    store = _get_store(collection_name)
    results = store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]