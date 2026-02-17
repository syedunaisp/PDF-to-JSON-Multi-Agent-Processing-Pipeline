"""
OCR Service - PyMuPDF Text Extraction with Tesseract OCR fallback
Extracts text directly from PDFs, with Tesseract OCR as fallback for images
"""
import os
import tempfile
from typing import List, Dict
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io

# Try to import pytesseract, but make it optional
try:
    import pytesseract
    # Set Tesseract path for Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# Tesseract configuration for better performance and multi-language support
TESSERACT_CONFIG = '--oem 3 --psm 6'  # LSTM OCR Engine, Assume uniform block of text


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> List[Dict[str, any]]:
    """
    Extract text from PDF bytes. First tries direct text extraction,
    falls back to OCR if needed.
    
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
        
        # First, try to extract text directly (works for text-based PDFs)
        text = page.get_text()
        
        # If no text found and Tesseract is available, try OCR
        if not text.strip() and TESSERACT_AVAILABLE:
            try:
                # Convert page to image (150 DPI for faster processing)
                mat = fitz.Matrix(150/72, 150/72)
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_bytes = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_bytes))
                
                # Run OCR with optimized config
                text = pytesseract.image_to_string(image, config=TESSERACT_CONFIG)
            except Exception as e:
                text = f"[OCR Error: {str(e)}]"
        
        results.append({
            "page": page_num + 1,
            "text": text.strip(),
            "status": "success" if text.strip() else "empty"
        })
    
    pdf_document.close()
    return results


def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, any]]:
    """
    Extract text from PDF file.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of dictionaries with page number and extracted text
    """
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    
    return extract_text_from_pdf_bytes(pdf_bytes)


def ocr_image_bytes(image_bytes: bytes) -> str:
    """
    Extract text from image bytes.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        Extracted text from the image
    """
    if not TESSERACT_AVAILABLE:
        return "[Tesseract not installed - text extraction only works for text-based PDFs]"
    
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run OCR with Tesseract (optimized config)
        text = pytesseract.image_to_string(image, config=TESSERACT_CONFIG)
        
        return text.strip()
    except Exception as e:
        raise Exception(f"OCR error: {str(e)}")
