from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from backend.rag.document_loader import (
    load_documents,
    split_documents,
)


CHROMA_DIR = "data/chroma"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store():
    documents = load_documents()
    chunks = split_documents(documents)

    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name="engineerflow_knowledge",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    vector_store.add_documents(chunks)

    return vector_store


def get_vector_store():
    embeddings = get_embeddings()

    return Chroma(
        collection_name="engineerflow_knowledge",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )