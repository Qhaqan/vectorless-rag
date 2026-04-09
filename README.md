# 📄 Vectorless RAG (PageIndex-Style) – PDF Question Answering System

## 🚀 Overview

This project demonstrates a **true vectorless RAG (Retrieval-Augmented Generation)** system inspired by **PageIndex.ai**.

Unlike traditional RAG systems that rely on:
- ❌ Embeddings
- ❌ Vector databases (FAISS, Pinecone, etc.)
- ❌ Similarity search

This system uses:
- ✅ Document structure (tree-based representation)
- ✅ LLM reasoning to locate relevant sections
- ✅ Context-based answer generation

---

## 🧠 How It Works (Architecture)

### Traditional RAG (NOT used here)
```
PDF → Chunking → Embeddings → Vector DB → Similarity Search → Answer
```

### Vectorless RAG (THIS PROJECT)
```
PDF → Text Extraction → Structured Tree → LLM Reasoning → Relevant Sections → Answer
```

---

## ⚙️ Features

- 📄 Upload any PDF
- 🌳 Automatically builds document structure
- 🧠 Uses LLM to select relevant sections
- 💬 Ask natural language questions
- ⚡ No vector database required
- 🔍 Explainable retrieval (shows selected section IDs)

---

## 📦 Requirements

Create a `requirements.txt` file:

```
fastapi==0.111.0
uvicorn==0.30.1
pypdf==4.2.0
openai==1.35.13
python-multipart==0.0.9
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup API Key

Edit your Python file and add your API key:

```python
openai.api_key = "YOUR_OPENAI_API_KEY"
```

👉 You can also replace OpenAI with:
- Groq (recommended for free usage)
- Azure OpenAI

---

## ▶️ Running the App

Start the server:

```bash
python app.py
```

Open in browser:

```
http://localhost:8000
```

---

## 🧪 How to Use

### Step 1: Upload PDF
- Click "Upload"
- System extracts text
- Builds internal tree structure

### Step 2: Ask Question
- Enter your question
- LLM selects relevant sections
- Answer is generated from those sections

---

## 🏗️ Core Components

### 1. PDF Extraction
```python
def extract_text(pdf_file):
```
Extracts raw text from uploaded PDF.

---

### 2. Tree Builder (IMPORTANT)
```python
def build_tree(text):
```
- Splits document into logical sections
- Creates structure like:

```
[
  {"id": 1, "title": "Introduction...", "content": "..."},
  {"id": 2, "title": "Methodology...", "content": "..."}
]
```

---

### 3. LLM-Based Retrieval (CORE IDEA)
```python
def select_relevant_nodes(query, tree):
```
- Sends document structure to LLM
- LLM decides which sections are relevant
- Returns section IDs

👉 This replaces embeddings completely

---

### 4. Answer Generation
```python
def generate_answer(query, context):
```
- Uses selected sections as context
- Generates final answer

---

## 🔍 Why This Is Better (In Some Cases)

| Feature | Vector RAG | Vectorless RAG |
|--------|------------|---------------|
| Setup | Complex | Simple |
| DB Required | Yes | No |
| Explainability | Low | High |
| Cost | Higher | Lower |
| Accuracy (structured docs) | Medium | High |

---

## ⚠️ Limitations

This is a **learning implementation**, not full PageIndex:

- Tree is basic (split by paragraphs)
- No multi-level hierarchy (chapters → sections)
- Single-step reasoning only
- Depends on LLM quality

---

## 🚀 Future Improvements

You can extend this system with:

- 🌳 Multi-level tree (chapters, headings)
- 🔁 Recursive reasoning (multi-hop retrieval)
- 🧾 JSON structured outputs
- ⚡ Streaming responses
- 📚 Multi-PDF support
- 💬 Chat history memory
- 🎨 Frontend (React / Vite)

---

## 🧩 Alternative: Real PageIndex API

Instead of building manually, you can use:

```bash
pip install pageindex
```

Example:

```python
from pageindex import PageIndexClient

client = PageIndexClient(api_key="YOUR_KEY")

doc = client.documents.create(file=open("file.pdf","rb").read())

result = client.documents.search(doc.id, "What is revenue?")
print(result)
```

---

## 🧠 Key Learning

This project teaches:

- How to build RAG without vectors
- How LLM reasoning can replace similarity search
- How document structure improves retrieval

---

## 📌 Summary

This is a **minimal, working implementation of PageIndex-style vectorless RAG**.

It proves that:

👉 You don’t need embeddings or vector DB to build intelligent document QA systems.

---

## 👨‍💻 Author Notes

Use this for:
- Learning advanced RAG concepts
- Prototyping AI document systems
- Building explainable AI pipelines

---

## 📬 Need Help?

If you want upgrades:
- Production-ready system
- Groq integration (free LLM)
- Full PageIndex clone
- UI like ChatGPT

👉 Just ask
