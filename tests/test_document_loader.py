from pathlib import Path

from backend.rag.document_loader import (
    load_documents,
    split_documents,
)

print("Current working directory:")
print(Path.cwd())

print("\nKnowledge directory:")
knowledge_dir = Path("knowledge")
print(knowledge_dir.resolve())

print("\nKnowledge directory exists:")
print(knowledge_dir.exists())

print("\nMarkdown files:")
for file_path in knowledge_dir.rglob("*.md"):
    print(file_path)


documents = load_documents()

print("\n=== Documents ===")
print(f"Number of documents: {len(documents)}")

chunks = split_documents(documents)

print("\n=== Chunks ===")
print(f"Number of chunks: {len(chunks)}")