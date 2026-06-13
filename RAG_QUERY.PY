import os
import sys
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

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


def query_memory(query, n_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    print("\nAION Evidence Retrieved\n")

    for i, doc in enumerate(documents):
        source = metadatas[i].get("source_file", "Unknown source")
        print(f"Evidence {i + 1}")
        print(f"Source: {source}")
        print(doc)
        print("-" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python rag_query.py "your query here"')
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    query_memory(user_query)