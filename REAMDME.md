# 📄 PDF-to-JSON Multi-Agent Processing Pipeline

## 📌 Project Overview

This project implements a **local, multi-agent document processing system** that converts PDF files into validated JSON output using OCR, reasoning-based LLMs, and schema validation.

The system is designed for reliability, modularity, and reproducibility, and is built using **LangChain, Lighton OCR, and Qwen3-14B Opus**.

---

## 🎯 Objective

To automate the transformation of unstructured PDF documents into structured, machine-readable JSON files through a multi-stage AI pipeline.

---

## 🧠 System Architecture

PDF
↓
Lighton OCR
↓
Raw Text
↓
Markdown Formatter
↓
Clean Markdown
↓
Qwen3-14B (LangChain Agent)
↓
JSON Schema Validation
↓
Final JSON Output


---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| Language | TypeScript (Node.js) |
| AI SDK | LangChain (JavaScript) |
| OCR Engine | Lighton OCR |
| LLM Model | Qwen3-14B Opus (GGUF / Local) |
| Validation | Zod / JSON Schema |
| Runtime | Local / Docker (Optional) |
| Output Format | JSON |

---

## 📂 Project Structure

pdf-to-json-pipeline/
│
├── ocr-service/ # Lighton OCR integration
├── markdown-formatter/ # OCR → Markdown processing
├── llm-parser/ # LangChain + Qwen parsing agent
├── validator/ # Schema validation and repair
├── orchestrator/ # Pipeline controller
├── config/ # Model and environment configs
└── README.md


---

## ⚙️ Pipeline Stages

### 1️⃣ OCR Extraction
- Converts PDF files into raw text and layout information using Lighton OCR.

### 2️⃣ Markdown Normalization
- Structures OCR output into clean Markdown format.
- Preserves headings, tables, and sections.

### 3️⃣ LLM-Based Parsing
- Uses Qwen3-14B Opus via LangChain.
- Converts Markdown into structured JSON.

### 4️⃣ Validation & Repair
- Validates output using Zod schemas.
- Automatically repairs invalid JSON using LLM reasoning.

### 5️⃣ Output Generation
- Produces final validated JSON file.

---

## 👥 Team Responsibilities

| Member | Module | Responsibility |
|--------|--------|----------------|
| Member 1 | OCR & Preprocessing | PDF → Markdown |
| Member 2 | LLM & LangChain | Markdown → JSON |
| Member 3 | Validation & Integration | JSON Verification & Pipeline |

---

## 🚀 Setup Instructions

### Prerequisites

- Node.js (v18+)
- npm / yarn
- Lighton OCR Access
- LM Studio / Ollama (for Qwen3-14B)
- Git

---

### Installation

```bash
git clone <repository-url>
cd pdf-to-json-pipeline
npm install
Environment Configuration
Create a .env file:

LLM_API_URL=http://localhost:1234
MODEL_NAME=qwen3-14b-opus
LIGHTON_API_KEY=your_key_here
Run Locally
npm run dev
Or using Docker:

docker build -t pdf-pipeline .
docker run -p 8000:8000 pdf-pipeline
📄 Usage
Place your PDF file in the input directory and run:

npm run process -- input.pdf
The final JSON output will be available in:

/output/final.json
✅ Features
Multi-agent architecture

Modular design

Local inference support

Schema validation

Automatic error recovery

Human-readable intermediate format

Reproducible pipeline
