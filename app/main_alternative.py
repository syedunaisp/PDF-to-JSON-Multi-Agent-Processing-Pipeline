import os
import tempfile
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import requests
from dotenv import load_dotenv
import fitz  # PyMuPDF
from PIL import Image

load_dotenv()

app = FastAPI(title="OCR Microservice (No Poppler Required)", version="2.0.0")

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/lightonai/LightOnOCR-2-1B"

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set")


def ocr_image_bytes(image_bytes: bytes) -> str:
    """Send image bytes to HF OCR API."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(HF_API_URL, headers=headers, data=image_bytes)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("generated_text", "")
    else:
        raise Exception(f"HF API error: {response.text}")


@app.get("/")
async def root():
    return {
        "message": "OCR Microservice is running (PyMuPDF - No Poppler needed)",
        "version": "2.0.0",
        "endpoints": {
            "/ocr": "Extract text from image",
            "/pdf-to-markdown": "Convert PDF to markdown (No Poppler required)"
        }
    }


@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from an uploaded image using Hugging Face OCR model."""
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
                "error": "Internal server error",
                "details": str(e)
            }
        )


@app.post("/pdf-to-markdown")
async def pdf_to_markdown(file: UploadFile = File(...)):
    """Convert PDF to markdown using OCR on each page (PyMuPDF - No Poppler needed)."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Read PDF content
        pdf_content = await file.read()
        
        # Open PDF with PyMuPDF
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Process each page
        markdown_content = ["# JEE Question Bank\n\n"]
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Convert page to image (300 DPI)
            mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PNG bytes
            img_bytes = pix.tobytes("png")
            
            try:
                text = ocr_image_bytes(img_bytes)
                markdown_content.append(f"## Page {page_num + 1}\n\n")
                markdown_content.append(text)
                markdown_content.append("\n\n---\n\n")
            except Exception as e:
                markdown_content.append(f"## Page {page_num + 1}\n\n")
                markdown_content.append(f"*Error: {e}*\n\n---\n\n")
        
        pdf_document.close()
        
        # Save markdown to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_md:
            tmp_md.write("".join(markdown_content))
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
