# OCR Service - DocTR Implementation

High-accuracy document OCR service using DocTR (90-94% accuracy) with excellent structure preservation.

## Features

- **High Accuracy**: 90-94% OCR accuracy using DocTR
- **Structure Preservation**: Maintains document layout and formatting
- **Batch Processing**: Processes 5 pages at a time with detailed logging
- **CPU Optimized**: Works efficiently on CPU without GPU
- **Windows Compatible**: Tested and working on Windows systems

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Note: First run will download DocTR models (~200MB), which may take a few minutes.

### 2. Run the Service
```bash
python orchestrator/api.py
```

The service will start at: **http://localhost:8001**

---

## Usage

### Option 1: Web Interface (Easiest)

1. Open http://localhost:8001/docs in your browser
2. Click on `/pdf-to-markdown` endpoint
3. Click "Try it out"
4. Upload your PDF file
5. Click "Execute"
6. Download the generated markdown file

### Option 2: Command Line

```bash
curl -X POST "http://localhost:8001/pdf-to-markdown" -F "file=@your_document.pdf" -o output.md
```

---

## Processing Details

The service processes PDFs in batches of 5 pages with detailed logging:

```
📚 PDF PROCESSING STARTED - Using DocTR
Total Pages: 67
Batch Size: 5 pages per batch
Total Batches: 14

📦 BATCH 1/14: Pages 1-5
  📄 Page 1: Running DocTR OCR...
  ✅ Page 1: DocTR completed (1234 characters)
  📄 Page 2: Running DocTR OCR...
  ✅ Page 2: DocTR completed (1456 characters)
  ...
  💾 Batch 1/14 completed - Memory cleared
  📊 Progress: 5/67 pages (7.5%)
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
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Python 3.8+ is required

**OCR not working?**
- First run downloads DocTR models (~200MB) - be patient
- Check internet connection for model download
- Ensure sufficient disk space for models

**Import errors?**
- Make sure you're running from the ocr-service directory
- Check that all dependencies are installed

**Memory issues with large PDFs?**
- The service processes 5 pages at a time to manage memory
- Each batch clears memory before processing the next batch
