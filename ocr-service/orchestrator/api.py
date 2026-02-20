"""
Orchestrator - FastAPI Service
Coordinates the entire PDF to Markdown pipeline
"""
import os
import sys

# Set environment variables before imports
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_use_cuda'] = '0'

import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import with underscore naming
from ocr_service.ocr_api import extract_text_from_pdf_bytes
from markdown_formatter.formatter import format_to_markdown

# Load environment from config folder
config_path = project_root / "config" / ".env"
load_dotenv(config_path)

app = FastAPI(
    title="PDF to Markdown OCR Service",
    description="Multi-stage pipeline for converting PDFs to structured markdown using OCR",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Health check and service information."""
    return {
        "service": "PDF to Markdown OCR Pipeline",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/ocr": "Extract text from single image",
            "/pdf-to-markdown": "Convert PDF to structured markdown"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    hf_token = os.getenv("HF_TOKEN")
    return {
        "status": "healthy",
        "hf_token_configured": bool(hf_token)
    }


@app.post("/ocr")
async def extract_text_from_image(file: UploadFile = File(...)):
    """
    Extract text from a single image using Surya OCR.
    
    Args:
        file: Image file upload
        
    Returns:
        JSON with extracted text
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    return JSONResponse(content={
        "success": False,
        "message": "Single image OCR endpoint temporarily disabled. Please use /pdf-to-markdown endpoint."
    })


@app.post("/pdf-to-markdown")
async def convert_pdf_to_markdown(file: UploadFile = File(...)):
    """
    Convert PDF to structured markdown using hybrid OCR approach.
    
    - Pix2Text: Mathematical formulas with LaTeX output
    - DocTR: Regular text with 90-94% accuracy
    
    Perfect for documents with mathematical expressions, equations, and formulas.
    
    Pipeline stages:
    1. OCR Extraction - Hybrid approach for text and math
    2. Markdown Formatting - Structure into clean markdown with LaTeX
    
    Args:
        file: PDF file upload
        
    Returns:
        Markdown file download with LaTeX formulas
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Read PDF bytes
        pdf_bytes = await file.read()
        print(f"Processing PDF: {file.filename}, size: {len(pdf_bytes)} bytes")
        
        # Process with hybrid OCR
        ocr_results = extract_text_from_pdf_bytes(pdf_bytes)
        
        # Format to markdown
        document_title = file.filename.replace('.pdf', '').replace('_', ' ').title()
        markdown_content = format_to_markdown(ocr_results, title=document_title)
        
        print(f"Markdown content length: {len(markdown_content)} characters")
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_md:
            tmp_md.write(markdown_content)
            tmp_md_path = tmp_md.name
        
        # Return markdown file
        return FileResponse(
            tmp_md_path,
            media_type="text/markdown",
            filename=file.filename.replace('.pdf', '.md')
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "PDF processing error",
                "details": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server on http://0.0.0.0:8001")
    print("PaddleOCR will be loaded on first OCR request (lazy loading)")
    uvicorn.run(app, host="0.0.0.0", port=8001)
