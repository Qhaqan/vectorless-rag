# ============================================
# TRUE VECTORLESS RAG (PAGEINDEX STYLE)
# ============================================
# pip install fastapi uvicorn pypdf openai

from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from pypdf import PdfReader
import uvicorn
import os
import openai

# ==============================
# CONFIG
# ==============================
openai.api_key = "YOUR_OPENAI_API_KEY"  # or Groq

app = FastAPI()

# In-memory tree
doc_tree = []

# ==============================
# STEP 1: EXTRACT PDF
# ==============================
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


# ==============================
# STEP 2: BUILD TREE (CORE LOGIC)
# ==============================
def build_tree(text):
    sections = text.split("\n\n")

    tree = []
    for i, sec in enumerate(sections):
        if len(sec.strip()) < 50:
            continue

        tree.append({
            "id": i,
            "title": sec[:80],
            "content": sec
        })

    return tree


# ==============================
# STEP 3: LLM REASONING (NO VECTOR)
# ==============================
def select_relevant_nodes(query, tree):

    tree_summary = "\n".join(
        [f"ID: {node['id']} | {node['title']}" for node in tree]
    )

    prompt = f"""
You are a document navigator.

Given this question:
{query}

Here is document structure:
{tree_summary}

Select top 3 most relevant section IDs.

Return ONLY numbers separated by commas.
Example: 2,5,9
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    ids = response["choices"][0]["message"]["content"]
    ids = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]

    return ids


# ==============================
# STEP 4: GENERATE ANSWER
# ==============================
def generate_answer(query, context):

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}

Give a precise answer.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response["choices"][0]["message"]["content"]


# ==============================
# ROUTES
# ==============================
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
    <body style="font-family: Arial; max-width:800px; margin:auto;">
        <h2>📄 Upload PDF (Vectorless RAG)</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>

        <h2>💬 Ask Question</h2>
        <form action="/ask" method="post">
            <input type="text" name="query" style="width:100%;" required>
            <button type="submit">Ask</button>
        </form>
    </body>
    </html>
    """


@app.post("/upload")
def upload(file: UploadFile):
    global doc_tree

    text = extract_text(file.file)
    doc_tree = build_tree(text)

    return {
        "message": "PDF processed (tree created)",
        "nodes": len(doc_tree)
    }


@app.post("/ask", response_class=HTMLResponse)
def ask(query: str = Form(...)):
    global doc_tree

    ids = select_relevant_nodes(query, doc_tree)

    selected_chunks = [
        node["content"] for node in doc_tree if node["id"] in ids
    ]

    context = "\n\n---\n\n".join(selected_chunks)

    answer = generate_answer(query, context)

    return f"""
    <html>
    <body style="font-family: Arial; max-width:800px; margin:auto;">
        <h3>🧠 Answer</h3>
        <pre>{answer}</pre>
        <p><b>Used Sections:</b> {ids}</p>
        <a href="/">⬅ Back</a>
    </body>
    </html>
    """


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
