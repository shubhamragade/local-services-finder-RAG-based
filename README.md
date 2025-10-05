# 🔍 Local Services RAG Assistant

A **Retrieval-Augmented Generation (RAG)** project that helps users find **local services** — like electricians, plumbers, or carpenters — near a specific area using **LangChain**, **ChromaDB**, **HuggingFace embeddings**, and **ChatGroq LLM**. 🧠⚡

---

## 🌟 Features

✅ Load local service data from CSV files (dummy data for Pune city).
✅ Generate embeddings for documents and store them in a **vector database (ChromaDB)**.
✅ Retrieve top-N relevant nearby services based on **category** and **distance**.
✅ Answer user queries using **retrieved documents + LLM**.
✅ Responds clearly — returns **“No nearby service found”** when nothing matches. 🙅‍♂️

---

## 🧱 Project Structure

```
├── data/                   # CSV files containing local services
│   ├── services_1.csv
│   ├── services_2.csv
│   └── services_3.csv
│
├── src/
│   ├── app.py              # Main script to run RAG assistant
│   └── vector.py           # VectorDB class for embeddings & retrieval
│
├── chroma_store/           # Persisted ChromaDB embeddings (auto-generated)
│
├── requirements.txt
└── README.md
```

---

## 🧾 Sample CSV Format

| name       | category    | area          | contact    | details       | distance |
| ---------- | ----------- | ------------- | ---------- | ------------- | -------- |
| ABC Shop   | Electrician | Shivaji Nagar | 1234567890 | 24/7 service  | 2.5      |
| XYZ Repair | Plumber     | XYZ Area      | 9876543210 | Fast response | 4.0      |

> ⚠️ **Note:** `distance` is in kilometers.

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone <repo_url>
cd rag-local-services
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ (Optional) Add environment variables

Create a `.env` file if you have API keys or environment settings.

```
# Example
API_KEY=<your_api_key_if_required>
```

---

## 🚀 Usage

Run the assistant:

```bash
python src/app.py
```

Then ask questions like 👇

```
Question: electrician near Shivaji Nagar
```

### 🧩 Sample Output

```
Here are the nearest electrician services near Shivaji Nagar:

1. ABC Electric → 24/7 service (Distance: 2.5 km)
2. XYZ Electric → Fast response (Distance: 3.2 km)
3. PQR Electric → Affordable (Distance: 4.8 km)
```

To exit, type:

```bash
exit
```

---

## 🧠 How It Works

1. Loads service data from multiple CSVs inside `data/`.
2. Generates **sentence embeddings** using `all-MiniLM-L6-v2`.
3. Stores embeddings in **ChromaDB** (persistent vector store).
4. On user query:

   * Uses **semantic search** to find top-matching services.
   * Optionally filters by category and distance.
   * Combines context with user query.
   * Passes to **ChatGroq LLM** for natural-language response.

---

## 🧩 Tech Stack

* 🦜 **LangChain** — for RAG pipeline and query orchestration.
* 🧮 **ChromaDB** — fast local vector storage.
* 🤗 **HuggingFace Embeddings** — `all-MiniLM-L6-v2`.
* ⚙️ **ChatGroq LLM** — lightweight large language model for reasoning.
* 📄 **Pandas** — for data loading and manipulation.

---

## 💡 Notes

* Automatically detects and merges all CSV files in `data/`.
* Filters irrelevant results based on **distance threshold** and **category match**. 🧭
* Returns simple JSON output — perfect for FastAPI or Streamlit integration.

---

## 🔮 Future Enhancements

✨ Add Streamlit UI with search box and category filters.
✨ Integrate live Google Maps API for location-based distance sorting.
✨ Cache embeddings to reduce load time.
✨ Add support for multilingual queries (Marathi, Hindi, etc.). 🌍

---

## 📜 License

MIT License — free to use, modify, and share. 💖

---

Would you like me to add a **Streamlit interface** for interactive search (with category + area dropdowns and distance slider)? 🎛️
