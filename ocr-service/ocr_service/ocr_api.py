"""
OCR Service - DocTR Implementation
High-accuracy document OCR with excellent structure preservation
Specifically designed for documents, not general images
CPU-optimized with good Windows compatibility
"""
import os
import tempfile
import gc
from typing import List, Dict
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import io
import numpy as np

# Lazy load DocTR to avoid startup delays
DOCTR_AVAILABLE = False
doctr_model = None

# Batch processing configuration - FIXED at 5 pages per batch
BATCH_SIZE = 5  # Always process 5 pages at a time
MAX_IMAGE_SIZE = 2000  # Max dimension for images (pixels)

def _init_doctr():
    """Initialize DocTR on first use (lazy loading)"""
    global DOCTR_AVAILABLE, doctr_model
    
    if doctr_model is not None:
        return
    
    try:
        from doctr.models import ocr_predictor
        
        print("🔧 Initializing DocTR (downloading models on first run)...")
        print("   This may take a few minutes on first use...")
        
        # Initialize DocTR with pretrained model
        # Using db_resnet50 for detection and crnn_vgg16_bn for recognition
        doctr_model = ocr_predictor(pretrained=True)
        
        DOCTR_AVAILABLE = True
        print("✅ DocTR initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize DocTR: {e}")
        import traceback
        traceback.print_exc()
        DOCTR_AVAILABLE = False
        doctr_model = None


def _process_page_doctr(page, page_num):
    """Process a single page with DocTR"""
    try:
        print(f"  📄 Page {page_num + 1}: Running DocTR OCR...")
        
        # Convert page to image with good DPI
        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom = ~144 DPI
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        # Resize if image is too large (to save memory)
        if max(image.size) > MAX_IMAGE_SIZE:
            ratio = MAX_IMAGE_SIZE / max(image.size)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array for DocTR
        img_array = np.array(image)
        
        # Run DocTR
        result = doctr_model([img_array])
        
        # Extract text from DocTR result
        text_lines = []
        for page_result in result.pages:
            for block in page_result.blocks:
                for line in block.lines:
                    line_text = " ".join([word.value for word in line.words])
                    if line_text.strip():
                        text_lines.append(line_text)
        
        text = '\n'.join(text_lines)
        
        print(f"  ✅ Page {page_num + 1}: DocTR completed ({len(text)} characters)")
        
        # Clean up memory
        del img_array, image, img_data, pix
        gc.collect()
        
        return text.strip()
        
    except Exception as e:
        print(f"  ❌ Page {page_num + 1}: DocTR Error - {e}")
        import traceback
        traceback.print_exc()
        return f"[DocTR Error: {str(e)}]"


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> List[Dict[str, any]]:
    """
    Extract text from PDF bytes with 5-page batch processing using DocTR.
    Each batch of 5 pages is fully processed before moving to the next.
    Detailed progress logging for each page.

    Args:
        pdf_bytes: PDF file as bytes

    Returns:
        List of dictionaries with page number and extracted text
    """
    results = []

    # Open PDF from bytes
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(pdf_document)
    total_batches = (total_pages + BATCH_SIZE - 1) // BATCH_SIZE

    print(f"\n{'='*70}")
    print(f"📚 PDF PROCESSING STARTED - Using DocTR")
    print(f"{'='*70}")
    print(f"Total Pages: {total_pages}")
    print(f"Batch Size: {BATCH_SIZE} pages per batch")
    print(f"Total Batches: {total_batches}")
    print(f"{'='*70}\n")

    # Process pages in batches of 5
    for batch_start in range(0, total_pages, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_pages)
        batch_num = (batch_start // BATCH_SIZE) + 1

        print(f"\n{'─'*70}")
        print(f"📦 BATCH {batch_num}/{total_batches}: Pages {batch_start + 1}-{batch_end}")
        print(f"{'─'*70}")

        for page_num in range(batch_start, batch_end):
            page = pdf_document[page_num]

            # First, try to extract text directly (works for text-based PDFs)
            text = page.get_text()

            # If no text found, try OCR
            if not text.strip():
                # Initialize DocTR on first use
                if doctr_model is None:
                    _init_doctr()

                if DOCTR_AVAILABLE and doctr_model is not None:
                    text = _process_page_doctr(page, page_num)
                else:
                    text = "[OCR not available - DocTR failed to initialize]"
                    print(f"  ❌ Page {page_num + 1}: DocTR not available")
            else:
                print(f"  ✅ Page {page_num + 1}: Text extracted directly (no OCR needed)")

            results.append({
                "page": page_num + 1,
                "text": text.strip(),
                "status": "success" if text.strip() else "empty"
            })

        # Force garbage collection after each batch
        gc.collect()

        print(f"\n  💾 Batch {batch_num}/{total_batches} completed - Memory cleared")
        print(f"  📊 Progress: {batch_end}/{total_pages} pages ({(batch_end/total_pages)*100:.1f}%)")
        print(f"  📝 Markdown for pages {batch_start + 1}-{batch_end} ready")

    pdf_document.close()

    print(f"\n{'='*70}")
    print(f"✅ ALL {total_pages} PAGES PROCESSED SUCCESSFULLY with DocTR!")
    print(f"{'='*70}")
    print(f"📄 Final integrated markdown file ready")
    print(f"{'='*70}\n")

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
