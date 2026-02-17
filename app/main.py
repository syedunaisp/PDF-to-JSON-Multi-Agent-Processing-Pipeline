import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="OCR Microservice", version="1.0.0")

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/lightonai/LightOnOCR-2-1B"

if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set")


@app.get("/")
async def root():
    return {"message": "OCR Microservice is running", "endpoint": "/ocr"}


@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    """
    Extract text from an uploaded image using Hugging Face OCR model.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_bytes = await file.read()
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        response = requests.post(HF_API_URL, headers=headers, data=image_bytes)
        
        if response.status_code == 200:
            result = response.json()
            return JSONResponse(content={
                "success": True,
                "filename": file.filename,
                "extracted_text": result.get("generated_text", ""),
                "raw_response": result
            })
        else:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "success": False,
                    "error": "Hugging Face API error",
                    "details": response.text,
                    "status_code": response.status_code
                }
            )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )
