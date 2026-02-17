# 📄 PDF-to-JSON Multi-Agent Processing Pipeline

## 📌 Project Overview

This project implements a **multi-agent document processing system** that converts PDF files into validated JSON output using OCR, reasoning-based LLMs, and schema validation.

---

## 📂 Project Structure

```
pdf-to-json-pipeline/
│
├── ocr-service/              # ✅ Member 1: OCR & Markdown Processing
│   ├── ocr_service/          # OCR extraction module
│   ├── markdown_formatter/   # Markdown formatting module
│   ├── orchestrator/         # FastAPI service
│   ├── config/              # Environment configuration
│   ├── requirements.txt     # Dependencies
│   └── README.md            # Setup instructions
│
├── validation-service/       # 🔄 Member 3: JSON Validation
│   └── src/                 # Validation and repair logic
│
└── README.md                # This file
```

---

## 👥 Team Responsibilities

| Member | Module | Status | Description |
|--------|--------|--------|-------------|
| Member 1 | ocr-service/ | ✅ Complete | PDF → Markdown conversion |
| Member 2 | llm-parser/ | 🔄 Pending | Markdown → JSON with LangChain |
| Member 3 | validation-service/ | 🔄 In Progress | JSON validation & repair |

---

## 🚀 Getting Started

### Member 1: OCR Service

```bash
cd ocr-service
pip install -r requirements.txt
cp config/.env.example config/.env
# Add your HF_TOKEN to config/.env
python orchestrator/api.py
```

Service runs at: http://localhost:8000

See `ocr-service/README.md` for detailed instructions.

---

## 🧠 System Architecture

```
PDF
 ↓
OCR Service (Member 1) → Markdown
 ↓
LLM Parser (Member 2) → JSON
 ↓
Validation Service (Member 3) → Validated JSON
```

---

## 📝 License

MIT License
