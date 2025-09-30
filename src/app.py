import os
import pandas as pd
from dotenv import load_dotenv
from typing import List
from vector import VectorDB
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseRetriever, Document
from pydantic import Field

load_dotenv()


# ---------- Load CSV documents ----------
def load_documents(data_dir="data") -> List[dict]:
    documents = []

    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"The directory {data_dir} does not exist.")

    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        if not os.path.isfile(file_path) or not file.endswith(".csv"):
            continue

        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            content = f"{row['name']} is a {row['category']} in {row['area']}. " \
                      f"Details: {row['details']}. Distance: {row['distance']} km."
            metadata = {
                "name": row["name"],
                "category": row["category"],
                "area": row["area"],
                "contact": row["contact"],
                "distance": float(row["distance"]),
                "source_file": file
            }
            documents.append({"content": content, "metadata": metadata})

    return documents


# ---------- Initialize VectorDB ----------
vdb = VectorDB()
docs = load_documents("data")
print(f"Loaded {len(docs)} documents.")
vdb.add_documents(docs)
print("Documents added to vector database.")


# ---------- Retriever ----------
class SimpleRetriever(BaseRetriever):
    vector_db: any = Field(...)
    n_results: int = Field(default=3)
    max_distance: float = Field(default=10.0)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        # Simple keyword parsing for category/area
        category = None
        area = None
        q_lower = query.lower()

        # Categories - adjust to your CSV
        for cat in ["electrician", "plumber", "carpenter"]:
            if cat in q_lower:
                category = cat

        # Areas - adjust to your CSV
        for a in ["shivaji nagar", "xyz area"]:
            if a in q_lower:
                area = a

        results = self.vector_db.search(
            query=query,
            n_results=self.n_results,
            max_distance=self.max_distance,
            category=category,
            area=area
        )

        return [Document(page_content=r["page_content"], metadata=r["metadata"]) for r in results]


# ---------- Initialize LLM ----------
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt_template = ChatPromptTemplate.from_template(
    "You are a local assistant. Answer the question using ONLY the nearby services below.\n\n"
    "Nearby Services:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer clearly. If no services match, say: 'No nearby service found.'"
)

retriever = SimpleRetriever(vector_db=vdb, n_results=3, max_distance=10)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)


# ---------- Run Interactive ----------
if __name__ == "__main__":
    print("Type your questions (or 'exit' to quit).")
    while True:
        q = input("\nQuestion: ")
        if q.lower() == "exit":
            break

        result = qa_chain.invoke({"query": q})

        print("\nAnswer:", result['result'])
        print("\nRetrieved Documents:")
        for doc in result['source_documents']:
            print("-", doc.metadata["name"], "->", doc.page_content[:100], "...")
