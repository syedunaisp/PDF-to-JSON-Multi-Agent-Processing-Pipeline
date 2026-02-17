"""
Markdown Formatter - OCR → Markdown Processing
Structures OCR output into clean Markdown format
"""
from typing import List, Dict


def format_to_markdown(ocr_results: List[Dict[str, any]], title: str = "Document") -> str:
    """
    Convert OCR results to structured markdown.
    
    Args:
        ocr_results: List of OCR results from ocr-service
        title: Document title for markdown header
        
    Returns:
        Formatted markdown string
    """
    markdown_lines = []
    
    # Add title
    markdown_lines.append(f"# {title}\n\n")
    
    # Process each page
    for result in ocr_results:
        page_num = result.get("page", 0)
        text = result.get("text", "")
        status = result.get("status", "unknown")
        
        markdown_lines.append(f"## Page {page_num}\n\n")
        
        if status == "success" and text:
            markdown_lines.append(text)
            markdown_lines.append("\n\n")
        elif status == "error":
            error = result.get("error", "Unknown error")
            markdown_lines.append(f"*Error extracting text: {error}*\n\n")
        else:
            markdown_lines.append("*No text extracted*\n\n")
        
        markdown_lines.append("---\n\n")
    
    return "".join(markdown_lines)


def save_markdown(markdown_content: str, output_path: str) -> None:
    """
    Save markdown content to file.
    
    Args:
        markdown_content: Markdown string
        output_path: Path to save the markdown file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
