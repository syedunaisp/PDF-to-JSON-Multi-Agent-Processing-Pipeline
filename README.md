# 📄 PDF-to-JSON Multi-Agent Processing Pipeline

## 📌 Project Overview

This project implements a **multi-agent document processing system** that converts PDF files into validated JSON output using OCR, reasoning-based LLMs, and schema validation.

The system is designed for reliability, modularity, and reproducibility, built using **Python, FastAPI, LightOn OCR (via Hugging Face), and LangChain**.

---

## 🎯 Objective

To automate the transformation of unstructured PDF documents (JEE question banks) into structured, machine-readable JSON files through a multi-stage AI pipeline.

---

## 🧠 System Architecture

```
PDF
 ↓
Lighton OCR (Hugging Face API)
 ↓
Raw Text
 ↓
Markdown Formatter
 ↓
Clean Markdown
 ↓
LangChain Agent (Future)
 ↓
JSON Schema Validation (Future)
 ↓
Final JSON Output
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Web Framework | FastAPI |
| OCR Engine | LightOn OCR (Hugging Face API) |
| PDF Processing | PyMuPDF |
| LLM SDK | LangChain (Future) |
| Validation | Pydantic / JSON Schema (Future) |
| Runtime | Local / Docker (Optional) |
| Output Format | Markdown → JSON |

---

## 📂 Project Structure

```
pdf-to-json-pipeline/
│
├── ocr_service/           # ✅ LightOn OCR integration (Member 1)
│   ├── __init__.py
│   └── ocr_api.py         # OCR API calls
│
├── markdown_formatter/    # ✅ OCR → Markdown processing (Member 1)
│   ├── __init__.py
│   └── formatter.py       # Markdown structuring
│
├── orchestrator/          # ✅ Pipeline controller (Member 1)
│   └── api.py            # FastAPI service
│
├── validation-service/    # 🔄 Schema validation (Member 3)
│   └── src/              # JSON validation and repair
│
├── config/               # Configuration
│   └── .env.example      # Environment template
│
├── requirements.txt      # Python dependencies
└── README.md
```
│   └── validator.py      # JSON validation and repair
│
├── orchestrator/         # Pipeline controller
│   └── api.py           # FastAPI service
│
├── config/              # Configuration
│   └── .env.example     # Environment template
│
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ⚙️ Current Pipeline Stages

### ✅ 1️⃣ OCR Extraction (Implemented)
- Converts PDF pages to images using PyMuPDF
- Extracts text using LightOn OCR via Hugging Face API
- No local GPU required

### ✅ 2️⃣ Markdown Normalization (Implemented)
- Structures OCR output into clean Markdown format
- Preserves page structure and sections

### 🔄 3️⃣ LLM-Based Parsing (In Progress - Other Team Member)
- Will use LangChain with local/cloud LLM
- Converts Markdown into structured JSON

### 🔄 4️⃣ Validation & Repair (In Progress - validation-service/)
- Validates output using JSON schemas
- Automatically repairs invalid JSON

### 🔄 5️⃣ Output Generation (Future)
- Produces final validated JSON file

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10+
- Hugging Face account and API token
- pip or conda

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/syedunaisp/PDF-to-JSON-Multi-Agent-Processing-Pipeline.git
cd PDF-to-JSON-Multi-Agent-Processing-Pipeline
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp config/.env.example config/.env
```

Edit `config/.env` and add your Hugging Face token:
```
HF_TOKEN=hf_your_actual_token_here
```

4. **Run the service**
```bash
cd orchestrator
python api.py
```

Or with uvicorn:
```bash
uvicorn orchestrator.api:app --reload --port 8000
```

---

## 📄 Usage

### API Endpoints

The service runs at `http://localhost:8000`

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

#### 2. OCR Single Image
```bash
curl -X POST "http://localhost:8000/ocr" \
  -F "file=@image.png"
```

#### 3. Convert PDF to Markdown
```bash
curl -X POST "http://localhost:8000/pdf-to-markdown" \
  -F "file=@jee_questions.pdf" \
  -o output.md
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI

---

## 🔧 Development Status

| Module | Status | Owner | Description |
|--------|--------|-------|-------------|
| OCR Service | ✅ Complete | Member 1 | PDF → Text extraction |
| Markdown Formatter | ✅ Complete | Member 1 | Text → Structured markdown |
| Orchestrator | ✅ Complete | Member 1 | API service |
| LLM Parser | 🔄 In Progress | Member 2 | Markdown → JSON |
| Validation Service | 🔄 In Progress | Member 3 | JSON validation |

---

## 🎯 Next Steps

1. **LLM Integration (Member 2)**
   - Add LLM parser for Markdown → JSON conversion
   - Support for local models (Ollama) or cloud APIs

2. **Complete Validation Service (Member 3)**
   - Finalize JSON schema for JEE questions
   - Complete validation and auto-repair logic

3. **Pipeline Integration**
   - Connect all stages
   - Add error handling and retry logic

---

## 👥 Team Responsibilities

| Member | Module | Responsibility |
|--------|--------|----------------|
| Member 1 | OCR & Preprocessing | ✅ PDF → Markdown |
| Member 2 | LLM & LangChain | 🔄 Markdown → JSON |
| Member 3 | Validation & Integration | 🔄 JSON Verification |

---

## ✅ Features

- ✅ Multi-stage architecture
- ✅ Modular design
- ✅ Cloud-based OCR (no GPU needed)
- ✅ FastAPI REST API
- ✅ Structured markdown output
- 🔄 Schema validation (planned)
- 🔄 LLM integration (planned)
- 🔄 Docker support (planned)

---

## 📝 License

MIT License

---

## 🤝 Contributing

Contributions are welcome! Please follow the modular structure and add tests for new features.
