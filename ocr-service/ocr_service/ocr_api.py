"""
OCR Service - PyMuPDF Text Extraction with PaddleOCR fallback
Extracts text directly from PDFs, with PaddleOCR as fallback for images
PaddleOCR supports 80+ languages and handles complex layouts better
"""
import os
import tempfile
from typing import List, Dict
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import numpy as np

# Try to import PaddleOCR
try:
    from paddleocr import PaddleOCR
    import paddle
    
    # Force CPU mode and disable oneDNN completely
    paddle.set_device('cpu')
    
    # Disable all oneDNN optimizations via Paddle's config
    try:
        from paddle.fluid import core
        core.set_flags({'FLAGS_use_mkldnn': False})
    except:
        pass
    
    # Initialize PaddleOCR with minimal parameters
    # use_angle_cls=True helps with rotated text
    # lang='en' for English
    ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False
    ocr_engine = None


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> List[Dict[str, any]]:
    """
    Extract text from PDF bytes. First tries direct text extraction,
    falls back to PaddleOCR if needed.
    
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
        
        # If no text found and PaddleOCR is available, try OCR
        if not text.strip() and PADDLE_AVAILABLE:
            try:
                # Convert page to image (higher DPI for better OCR)
                mat = fitz.Matrix(2, 2)  # 2x zoom = ~144 DPI
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to numpy array for PaddleOCR
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                img_array = np.array(image)
                
                # Run PaddleOCR (no cls parameter, it's set during initialization)
                result = ocr_engine.ocr(img_array)
                
                # Extract text from PaddleOCR result
                if result and result[0]:
                    text_lines = []
                    for line in result[0]:
                        if line[1][0]:  # line[1][0] contains the text
                            text_lines.append(line[1][0])
                    text = '\n'.join(text_lines)
                
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
    Extract text from image bytes using PaddleOCR.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        Extracted text from the image
    """
    if not PADDLE_AVAILABLE:
        return "[PaddleOCR not installed - text extraction only works for text-based PDFs]"
    
    try:
        # Convert bytes to PIL Image then to numpy array
        image = Image.open(io.BytesIO(image_bytes))
        img_array = np.array(image)
        
        # Run PaddleOCR (no cls parameter)
        result = ocr_engine.ocr(img_array)
        
        # Extract text from result
        if result and result[0]:
            text_lines = []
            for line in result[0]:
                if line[1][0]:
                    text_lines.append(line[1][0])
            return '\n'.join(text_lines)
        
        return ""
        
    except Exception as e:
        raise Exception(f"OCR error: {str(e)}")
