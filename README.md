# 🏥 Medical Chatbot

A RAG-based (Retrieval-Augmented Generation) medical chatbot that answers questions from a medical PDF book using local embeddings and a free LLM via OpenRouter.

---

## 🧠 How It Works

```
User Question
     │
     ▼
HuggingFace Embeddings (local)
     │
     ▼
ChromaDB Vector Search → Relevant Medical Context
     │
     ▼
OpenRouter (nvidia/nemotron-3-nano-30b-a3b:free)
     │
     ▼
Answer
```

1. `ingest.py` loads the medical PDF, splits it into chunks, embeds them locally using `all-MiniLM-L6-v2`, and stores them in a ChromaDB vector database.
2. `main.py` runs a FastAPI server. When a question is received, it retrieves the most relevant chunks from ChromaDB and sends them as context to the LLM.
3. The LLM (via OpenRouter) generates an answer grounded in the retrieved medical context.

---

## 🗂️ Project Structure

```
Medical-chatbot-1/
├── backend/
│   ├── data/
│   │   └── Medical_book.pdf       # Your medical PDF source
│   ├── chroma_db/                 # Auto-generated vector database
│   ├── ingest.py                  # PDF ingestion & embedding script
│   ├── main.py                    # FastAPI backend server
│   ├── .env                       # API keys (not committed to git)
│   └── requirements.txt
├── frontend/                      # React frontend
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (local) |
| Vector Store | ChromaDB |
| LLM | `nvidia/nemotron-3-nano-30b-a3b:free` via OpenRouter |
| PDF Loader | LangChain PyPDFLoader |
| Frontend | React |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Medical-chatbot-1.git
cd Medical-chatbot-1
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend/` folder:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your free API key at [https://openrouter.ai](https://openrouter.ai)

### 5. Add Your Medical PDF

Place your PDF file in:
```
backend/data/Medical_book.pdf
```

### 6. Ingest the PDF

This will embed the PDF and create the local vector database:

```bash
python ingest.py
```

> ⚠️ First run will download the `all-MiniLM-L6-v2` model (~80MB). This is a one-time download.

Expected output:
```
Loading and processing: .../Medical_book.pdf
📄 Total chunks to embed: 1234
🔄 Loading embedding model...
Creating vector database...
✅ Success! Database saved to .../chroma_db
```

### 7. Start the Backend Server

```bash
python -m uvicorn main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

### 8. Start the Frontend

```bash
cd ../frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

---

## 📡 API Reference

### `GET /`
Health check endpoint.

**Response:**
```json
{ "status": "Medical chatbot API is running" }
```

### `POST /chat`
Ask a medical question.

**Request Body:**
```json
{ "question": "What are the symptoms of diabetes?" }
```

**Response:**
```json
{ "answer": "Diabetes symptoms include increased thirst, frequent urination..." }
```

---

## 📦 Requirements

Create a `requirements.txt` with:

```txt
fastapi
uvicorn
python-dotenv
langchain
langchain-community
langchain-core
langchain-chroma
langchain-huggingface
sentence-transformers
openai
pypdf
chromadb
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🔑 Getting a Free OpenRouter API Key

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Navigate to **API Keys** and create a new key
4. Paste it into your `.env` file

The model `nvidia/nemotron-3-nano-30b-a3b:free` is completely free with no billing required.

---

## ❓ Troubleshooting

**`chroma_db` not found error**
→ Run `python ingest.py` before starting the server.

**Rate limit errors during ingestion**
→ The ingestion uses local embeddings so there are no API rate limits. If you switch back to a cloud embedding model, add delays between batches.

**`ModuleNotFoundError`**
→ Make sure your virtual environment is activated before installing packages and running scripts.

**Model not found error**
→ Verify your `OPENROUTER_API_KEY` is set correctly in `.env` and the key is active.

---

## 📄 License

MIT License — feel free to use and modify for your own projects.