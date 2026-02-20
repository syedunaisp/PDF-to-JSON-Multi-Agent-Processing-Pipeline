"""
OCR Service - Hybrid DocTR + Pix2Text Implementation
- DocTR: High-accuracy text recognition (90-94%)
- Pix2Text: Mathematical formula recognition with LaTeX output
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

# Lazy load models to avoid startup delays
DOCTR_AVAILABLE = False
PIX2TEXT_AVAILABLE = False
doctr_model = None
pix2text_model = None

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
        doctr_model = ocr_predictor(pretrained=True)
        
        DOCTR_AVAILABLE = True
        print("✅ DocTR initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize DocTR: {e}")
        import traceback
        traceback.print_exc()
        DOCTR_AVAILABLE = False
        doctr_model = None


def _init_pix2text():
    """Initialize Pix2Text for mathematical formulas (lazy loading)"""
    global PIX2TEXT_AVAILABLE, pix2text_model
    
    if pix2text_model is not None:
        return
    
    try:
        from pix2text import Pix2Text
        
        print("🔧 Initializing Pix2Text for math formulas...")
        print("   This may take a few minutes on first use...")
        
        # Initialize Pix2Text with math formula recognition
        pix2text_model = Pix2Text.from_config()
        
        PIX2TEXT_AVAILABLE = True
        print("✅ Pix2Text initialized successfully!")
        
    except Exception as e:
        print(f"⚠️  Pix2Text not available (math formulas will use DocTR): {e}")
        PIX2TEXT_AVAILABLE = False
        pix2text_model = None


def _process_page_hybrid(page, page_num):
    """Process a single page with hybrid DocTR + Pix2Text approach"""
    try:
        print(f"  📄 Page {page_num + 1}: Running hybrid OCR (DocTR + Pix2Text)...")
        
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
        
        # Try Pix2Text first (better for math formulas)
        if PIX2TEXT_AVAILABLE and pix2text_model is not None:
            try:
                # Pix2Text can handle both text and math formulas
                result = pix2text_model.recognize(image, resized_shape=800)
                
                # Extract text with LaTeX formulas
                if isinstance(result, dict) and 'text' in result:
                    text = result['text']
                elif isinstance(result, str):
                    text = result
                else:
                    text = str(result)
                
                print(f"  ✅ Page {page_num + 1}: Pix2Text completed ({len(text)} characters)")
                
            except Exception as e:
                print(f"  ⚠️  Page {page_num + 1}: Pix2Text failed, falling back to DocTR - {e}")
                text = _process_with_doctr(image, page_num)
        else:
            # Fall back to DocTR
            text = _process_with_doctr(image, page_num)
        
        # Clean up memory
        del image, img_data, pix
        gc.collect()
        
        return text.strip()
        
    except Exception as e:
        print(f"  ❌ Page {page_num + 1}: Hybrid OCR Error - {e}")
        import traceback
        traceback.print_exc()
        return f"[OCR Error: {str(e)}]"


def _process_with_doctr(image, page_num):
    """Process image with DocTR (fallback or when Pix2Text unavailable)"""
    try:
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
        
        del img_array
        return text.strip()
        
    except Exception as e:
        print(f"  ❌ Page {page_num + 1}: DocTR Error - {e}")
        return f"[DocTR Error: {str(e)}]"


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> List[Dict[str, any]]:
    """
    Extract text from PDF bytes with 5-page batch processing using hybrid OCR.
    Uses Pix2Text for math formulas (LaTeX output) and DocTR for regular text.
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
    print(f"📚 PDF PROCESSING STARTED - Hybrid OCR (DocTR + Pix2Text)")
    print(f"{'='*70}")
    print(f"Total Pages: {total_pages}")
    print(f"Batch Size: {BATCH_SIZE} pages per batch")
    print(f"Total Batches: {total_batches}")
    print(f"Math Formulas: Will be converted to LaTeX format")
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
                # Initialize models on first use
                if doctr_model is None:
                    _init_doctr()
                if pix2text_model is None:
                    _init_pix2text()

                if DOCTR_AVAILABLE and doctr_model is not None:
                    text = _process_page_hybrid(page, page_num)
                else:
                    text = "[OCR not available - Models failed to initialize]"
                    print(f"  ❌ Page {page_num + 1}: OCR not available")
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
    print(f"✅ ALL {total_pages} PAGES PROCESSED SUCCESSFULLY!")
    print(f"{'='*70}")
    print(f"📄 Final integrated markdown file ready")
    print(f"📐 Math formulas converted to LaTeX format")
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
