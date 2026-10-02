from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


KNOWLEDGE_DIR = Path("knowledge")


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.rglob("*.md"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8",
        )

        file_documents = loader.load()

        for document in file_documents:
            relative_path = file_path.relative_to(KNOWLEDGE_DIR)

            parts = relative_path.parts

            domain = parts[0]
            title = file_path.stem

            document.metadata["domain"] = domain
            document.metadata["title"] = title
            document.metadata["source"] = "EngineerFlow Knowledge Base"
            document.metadata["file_path"] = str(relative_path)

        documents.extend(file_documents)

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return splitter.split_documents(documents)