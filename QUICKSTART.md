# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp config/.env.example config/.env
```

Edit `config/.env` and add your Hugging Face token:
```
HF_TOKEN=hf_your_actual_token_here
```

Get your token from: https://huggingface.co/settings/tokens

### 3. Run the Service
```bash
python orchestrator/api.py
```

The service will start at: **http://localhost:8000**

---

## Usage

### Option 1: Web Interface (Easiest)

1. Open http://localhost:8000/docs in your browser
2. Click on `/pdf-to-markdown` endpoint
3. Click "Try it out"
4. Upload your JEE question bank PDF
5. Click "Execute"
6. Download the generated markdown file

### Option 2: Command Line

```bash
curl -X POST "http://localhost:8000/pdf-to-markdown" \
  -F "file=@your_jee_questions.pdf" \
  -o output.md
```

---

## What You Get

The service converts your PDF into structured markdown:

```markdown
# Your Document Title

## Page 1

[Extracted text from page 1...]

---

## Page 2

[Extracted text from page 2...]

---
```

This markdown output is ready for:
- LangChain processing (next stage)
- JSON conversion with LLM
- Schema validation

---

## Next Steps

The markdown file will be processed by:
1. **LLM Parser** (llm_parser/) - Convert markdown to JSON
2. **Validator** (validator/) - Validate and repair JSON

These modules are placeholders for now and will be implemented next.

---

## Troubleshooting

**Service won't start?**
- Check that HF_TOKEN is set in `config/.env`
- Verify all dependencies are installed: `pip install -r requirements.txt`

**OCR not working?**
- Verify your Hugging Face token is valid
- Check internet connection (API calls to Hugging Face)

**Import errors?**
- Make sure you're running from the project root directory
- Python 3.10+ is required
