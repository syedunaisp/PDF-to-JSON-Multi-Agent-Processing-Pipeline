# OCR Microservice

Production-ready OCR microservice using Hugging Face's LightOnOCR-2-1B model via Inference API.

## Features

- FastAPI backend with `/ocr` endpoint
- Hugging Face Inference API integration (no GPU required)
- Docker support
- Proper error handling
- Environment-based configuration

## Setup

### 1. Get Hugging Face Token

1. Create account at https://huggingface.co
2. Go to Settings → Access Tokens
3. Create a new token with read permissions

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your token:
```
HF_TOKEN=hf_your_actual_token_here
```

## Running Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Server

```bash
uvicorn main:app --reload
```

Server will start at `http://localhost:8000`

## Running with Docker

### Build Image

```bash
docker build -t ocr-microservice .
```

### Run Container

```bash
docker run -p 8000:8000 -e HF_TOKEN=your_token_here ocr-microservice
```

Or with `.env` file:

```bash
docker run -p 8000:8000 --env-file .env ocr-microservice
```

## API Usage

### Test Endpoint

```bash
curl http://localhost:8000/
```

### OCR Request

```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.png"
```

### Response Format

Success:
```json
{
  "success": true,
  "filename": "image.png",
  "extracted_text": "Text extracted from image...",
  "raw_response": {...}
}
```

Error:
```json
{
  "success": false,
  "error": "Error description",
  "details": "Detailed error message"
}
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Model Information

- Model: `lightonai/LightOnOCR-2-1B`
- Provider: Hugging Face Inference API
- No local GPU required
- API URL: https://api-inference.huggingface.co/models/lightonai/LightOnOCR-2-1B

## Notes

- First request may take longer (model loading on HF servers)
- Free tier has rate limits
- Supported image formats: PNG, JPG, JPEG, etc.
