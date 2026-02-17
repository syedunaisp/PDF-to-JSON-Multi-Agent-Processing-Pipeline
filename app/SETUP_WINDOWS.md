# Windows Setup for PDF Processing

## Install Poppler (Required for PDF to Image Conversion)

### Option 1: Using Chocolatey (Recommended)

```bash
choco install poppler
```

### Option 2: Manual Installation

1. Download Poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the ZIP file to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to your PATH environment variable

### Verify Installation

```bash
pdftoppm -v
```

## Usage

Once Poppler is installed, you can use the `/pdf-to-markdown` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/pdf-to-markdown" -F "file=@your_jee_questions.pdf" -o output.md
```

Or use the Swagger UI at http://127.0.0.1:8000/docs
