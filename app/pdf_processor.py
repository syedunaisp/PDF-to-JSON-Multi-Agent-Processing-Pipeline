import os
import requests
from pdf2image import convert_from_path
from dotenv import load_dotenv
import tempfile
from pathlib import Path

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/lightonai/LightOnOCR-2-1B"


def ocr_image(image_bytes: bytes) -> str:
    """Send image to Hugging Face OCR API and get text."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(HF_API_URL, headers=headers, data=image_bytes)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("generated_text", "")
    else:
        raise Exception(f"OCR API error: {response.text}")


def pdf_to_markdown(pdf_path: str, output_path: str = None) -> str:
    """
    Convert PDF to markdown using OCR.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Optional path for output markdown file
    
    Returns:
        Extracted text as markdown string
    """
    print(f"Converting PDF: {pdf_path}")
    
    # Convert PDF to images
    print("Converting PDF pages to images...")
    images = convert_from_path(pdf_path, dpi=300)
    print(f"Found {len(images)} pages")
    
    markdown_content = []
    markdown_content.append("# JEE Question Bank\n\n")
    
    # Process each page
    for i, image in enumerate(images, 1):
        print(f"Processing page {i}/{len(images)}...")
        
        # Save image to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            image.save(tmp.name, 'PNG')
            
            # Read image bytes
            with open(tmp.name, 'rb') as f:
                image_bytes = f.read()
            
            # OCR the image
            try:
                text = ocr_image(image_bytes)
                markdown_content.append(f"## Page {i}\n\n")
                markdown_content.append(text)
                markdown_content.append("\n\n---\n\n")
            except Exception as e:
                print(f"Error on page {i}: {e}")
                markdown_content.append(f"## Page {i}\n\n")
                markdown_content.append(f"*Error extracting text: {e}*\n\n")
                markdown_content.append("---\n\n")
            
            # Clean up temp file
            os.unlink(tmp.name)
    
    # Combine all content
    final_markdown = "".join(markdown_content)
    
    # Save to file if output path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_markdown)
        print(f"Markdown saved to: {output_path}")
    
    return final_markdown


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_processor.py <pdf_file> [output_file.md]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else pdf_file.replace('.pdf', '.md')
    
    if not os.path.exists(pdf_file):
        print(f"Error: File not found: {pdf_file}")
        sys.exit(1)
    
    try:
        markdown = pdf_to_markdown(pdf_file, output_file)
        print("\n✓ Conversion complete!")
        print(f"Output: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
