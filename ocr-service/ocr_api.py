"""
OCR Service - Lighton OCR Integration
Converts PDF pages to images and extracts text using Hugging Face OCR API
"""
import os
import tempfile
from typing import List, Dict
import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/lightonai/LightOnOCR-2-1B"


def ocr_image_bytes(image_bytes: bytes) -> str:
    """
    Send image bytes to Hugging Face OCR API.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        Extracted text from the image
    """
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN environment variable is not set")
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(HF_API_URL, headers=headers, data=image_bytes)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("generated_text", "")
    else:
        raise Exception(f"HF API error: {response.status_code} - {response.text}")


def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, any]]:
    """
    Extract text from PDF using OCR on each page.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of dictionaries with page number and extracted text
    """
    results = []
    
    # Open PDF with PyMuPDF
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Convert page to image (300 DPI)
        mat = fitz.Matrix(300/72, 300/72)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PNG bytes
        img_bytes = pix.tobytes("png")
        
        try:
            text = ocr_image_bytes(img_bytes)
            results.append({
                "page": page_num + 1,
                "text": text,
                "status": "success"
            })
        except Exception as e:
            results.append({
                "page": page_num + 1,
                "text": "",
                "status": "error",
                "error": str(e)
            })
    
    pdf_document.close()
    return results


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> List[Dict[str, any]]:
    """
    Extract text from PDF bytes using OCR on each page.
    
    Args:
        pdf_bytes: PDF file as bytes
        
    Returns:
        List of dictionaries with page number and extracted text
    """
    results = []
    
    # Open PDF from bytes
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Convert page to image (300 DPI)
        mat = fitz.Matrix(300/72, 300/72)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PNG bytes
        img_bytes = pix.tobytes("png")
        
        try:
            text = ocr_image_bytes(img_bytes)
            results.append({
                "page": page_num + 1,
                "text": text,
                "status": "success"
            })
        except Exception as e:
            results.append({
                "page": page_num + 1,
                "text": "",
                "status": "error",
                "error": str(e)
            })
    
    pdf_document.close()
    return results
