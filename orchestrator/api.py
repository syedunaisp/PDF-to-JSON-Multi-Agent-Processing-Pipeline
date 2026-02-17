"""
Orchestrator - FastAPI Service
Coordinates the entire PDF to Markdown pipeline
"""
import os
import sys
import tempfile
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ocr_service.ocr_api import extract_text_from_pdf_bytes, ocr_image_bytes
from markdown_formatter.formatter import format_to_markdown

load_dotenv()

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
    Extract text from a single image using OCR.
    
    Args:
        file: Image file upload
        
    Returns:
        JSON with extracted text
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_bytes = await file.read()
        text = ocr_image_bytes(image_bytes)
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "extracted_text": text
        })
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "OCR processing error",
                "details": str(e)
            }
        )


@app.post("/pdf-to-markdown")
async def convert_pdf_to_markdown(file: UploadFile = File(...)):
    """
    Convert PDF to structured markdown using OCR pipeline.
    
    Pipeline stages:
    1. OCR Extraction - Extract text from each page
    2. Markdown Formatting - Structure into clean markdown
    
    Args:
        file: PDF file upload
        
    Returns:
        Markdown file download
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Stage 1: OCR Extraction
        pdf_bytes = await file.read()
        ocr_results = extract_text_from_pdf_bytes(pdf_bytes)
        
        # Stage 2: Markdown Formatting
        document_title = file.filename.replace('.pdf', '').replace('_', ' ').title()
        markdown_content = format_to_markdown(ocr_results, title=document_title)
        
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
