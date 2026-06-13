import os
import pandas as pd
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = "rag_data/raw"
CHROMA_DIR = "chroma_db"

client = chromadb.PersistentClient(path=CHROMA_DIR)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="aion_evidence_memory",
    embedding_function=openai_ef
)


def chunk_text(text, chunk_size=900, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def read_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def read_csv(path):
    df = pd.read_csv(path)
    return df.astype(str).apply(lambda row: " | ".join(row), axis=1).tolist()


def ingest_file(file_path):
    filename = os.path.basename(file_path)
    ext = filename.lower().split(".")[-1]

    documents = []

    if ext == "pdf":
        text = read_pdf(file_path)
        documents = chunk_text(text)

    elif ext == "csv":
        rows = read_csv(file_path)
        for row in rows:
            documents.extend(chunk_text(row))

    elif ext in ["txt", "md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        documents = chunk_text(text)

    else:
        print(f"Skipping unsupported file: {filename}")
        return

    ids = []
    metadatas = []

    for i, doc in enumerate(documents):
        ids.append(f"{filename}_{i}")
        metadatas.append({
            "source_file": filename,
            "file_type": ext,
            "aion_layer": "evidence_memory"
        })

    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    print(f"Ingested {len(documents)} chunks from {filename}")


def main():
    for filename in os.listdir(RAW_DIR):
        file_path = os.path.join(RAW_DIR, filename)
        if os.path.isfile(file_path):
            ingest_file(file_path)

    print("AION Evidence Memory build complete.")


if __name__ == "__main__":
    main()