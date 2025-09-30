# Local Services RAG Assistant

This is a **Retrieval-Augmented Generation (RAG)** project to help users find **local services** (like electricians, plumbers, carpenters) near a specific area. It uses **LangChain**, **ChromaDB**, **HuggingFace embeddings**, and **ChatGroq LLM**.

---

## Features

- Load local service data from CSV files (dummy data for Pune city).
- Generate embeddings for documents and store them in a vector database (ChromaDB).
- Retrieve top-N relevant nearby services based on **category** and **distance**.
- Answer user queries using retrieved documents with a large language model (LLM).
- Returns a clear answer, or **“No nearby service found”** if nothing matches.

---

## Project Structure

├── data/ # CSV files containing local services
│ ├── services_1.csv
│ ├── services_2.csv
│ └── services_3.csv
├── src/
│ ├── app.py # Main script to run RAG assistant
│ └── vector.py # VectorDB class for Chroma embeddings and search
├── chroma_store/ # Persisted ChromaDB embeddings (auto-generated)
├── requirements.txt
└── README.md
>>>>>>> de72f2f (added update README.md)


## Sample CSV Format

Each CSV file should have the following columns:

| name       | category     | area          | contact     | details        | distance |
|------------|-------------|---------------|------------|----------------|---------|
| ABC Shop   | Electrician | Shivaji Nagar | 1234567890 | 24/7 service   | 2.5     |
| XYZ Repair | Plumber     | XYZ Area      | 9876543210 | Fast response  | 4.0     |

> **Note:** `distance` is in kilometers.


## Installation

1. Clone the repository:

```bash
git clone <repo_url>
cd rag-local-services
Create a virtual environment:

bash

python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
Install dependencies:

bash

pip install -r requirements.txt
Create a .env file if needed (optional):

env

# Example
# API_KEY=<your_key_if_required>
Usage
Run the RAG assistant:

bash
python src/app.py
Type your questions about local services, for example:


Question: electrician near Shivaji Nagar
Sample Output:


Here are the nearest electrician services near Shivaji Nagar:

1. ABC Electric -> 24/7 service (Distance: 2.5 km)
2. XYZ Electric -> Fast response (Distance: 3.2 km)
3. PQR Electric -> Affordable (Distance: 4.8 km)
To exit, type:

bash

The assistant will:

Search the vector database for top nearby services matching the query.

Answer using retrieved documents.

Show the relevant documents used for the answer.

Notes
Uses ChatGroq LLM.

Embeddings generated with all-MiniLM-L6-v2 model.

Supports distance filtering and category-based retrieval.

CSV files in data/ are automatically loaded and added to the vector database.
