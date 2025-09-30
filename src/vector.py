import uuid
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb


class VectorDB:
    def __init__(self, persist_dir="chroma_store"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("local_services")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to ChromaDB with embeddings."""
        for doc in documents:
            chunks = self.text_splitter.split_text(doc["content"])
            for chunk in chunks:
                embedding = self.embedding_model.encode(chunk).tolist()
                self.collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[doc["metadata"]],
                    ids=[str(uuid.uuid4())]
                )

    def search(
        self,
        query: str,
        n_results: int = 5,
        max_distance: float = None,
        category: str = None,
        area: str = None
    ) -> List[Dict[str, Any]]:
        """Search using embeddings and filter by metadata."""

        
        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results * 2,  
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        
        filtered_docs = []
        for doc, meta in zip(documents, metadatas):
            if category and category.lower() not in meta["category"].lower():
                continue
            if area and area.lower() not in meta["area"].lower():
                continue
            if max_distance is not None and float(meta["distance"]) > max_distance:
                continue
            filtered_docs.append({"page_content": doc, "metadata": meta})

        return filtered_docs[:n_results]
