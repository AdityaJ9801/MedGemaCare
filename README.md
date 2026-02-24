# Medical Report Analysis API

> **Production-grade FastAPI application for medical report summarization and analysis using Google's MedGemma model with RAG (Retrieval-Augmented Generation) capabilities.**

Built for doctors and healthcare professionals to efficiently analyze medical reports, extract insights, and generate summaries.

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Docker Deployment](#docker-deployment)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## ✨ Features

### Core Capabilities
- ✅ **Medical Report Summarization** - Generate concise summaries from lengthy medical reports
- ✅ **Question Answering** - Ask specific questions about medical reports and get accurate answers
- ✅ **Document Processing** - Support for PDF and text documents with automatic text extraction
- ✅ **Image Processing** - OCR support for medical images (scans, X-rays, handwritten notes)
- ✅ **RAG Support** - Handle large documents efficiently with vector-based retrieval
- ✅ **Multi-modal Support** - Process both text and image inputs

### Production Features
- ✅ **Modular Architecture** - Clean, maintainable, and scalable code structure
- ✅ **Type Safety** - Full type hints with Pydantic models
- ✅ **Error Handling** - Comprehensive exception handling and logging
- ✅ **API Documentation** - Interactive Swagger UI and ReDoc
- ✅ **Docker Support** - Easy deployment with Docker and Docker Compose
- ✅ **Testing** - Unit and integration tests with pytest
- ✅ **Logging** - Structured logging with rotation and levels
- ✅ **Configuration** - Environment-based configuration management
- ✅ **GPU Acceleration** - CUDA support with automatic fallback to CPU
- ✅ **Model Quantization** - 4-bit/8-bit quantization for memory efficiency

---

## 🚀 Quick Start

Get up and running in 5 minutes!

### Prerequisites
- Python 3.9+ installed
- (Optional) CUDA-capable GPU for faster inference
- At least 8GB RAM
- At least 10GB disk space

### Automated Setup (Recommended)

**Windows:**
```powershell
.\scripts\setup.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create configuration
cp .env.example .env

# 5. Create directories
mkdir models vector_store logs
```

### Run the API

```bash
python run.py
```

The API will start at `http://localhost:8000`

### Test the API

```bash
# Check health
curl http://localhost:8000/health

# Access interactive docs
# Open browser: http://localhost:8000/docs
```

---

## 📦 Installation

### Detailed Installation Steps

```bash
# 1. Clone the repository (if applicable)
git clone <repository-url>
cd hack-nagpur

# 2. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup configuration
cp .env.example .env

# 5. Create necessary directories
mkdir models vector_store logs
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false

# Model Configuration
MODEL_NAME=google/medgemma-2b
MODEL_DEVICE=cuda              # cuda or cpu
MODEL_QUANTIZATION=4bit        # 4bit, 8bit, or none
MAX_MODEL_LENGTH=2048
MODEL_CACHE_DIR=./models

# RAG Configuration
CHUNK_SIZE=512
CHUNK_OVERLAP=50
TOP_K_RETRIEVAL=5
VECTOR_STORE_PATH=./vector_store
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Document Processing
MAX_FILE_SIZE_MB=50
SUPPORTED_DOC_FORMATS=pdf,txt
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,tiff

# Logging
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
LOG_FILE=./logs/app.log
LOG_ROTATION=100 MB
LOG_RETENTION=30 days

# Security (Optional)
API_KEY_ENABLED=false
API_KEY=your-secret-api-key-here
CORS_ORIGINS=*
```

### Configuration Tips

**For CPU-only systems:**
```env
MODEL_DEVICE=cpu
MODEL_QUANTIZATION=4bit
```

**For GPU systems:**
```env
MODEL_DEVICE=cuda
MODEL_QUANTIZATION=4bit  # or 8bit for better quality
```

**For production:**
```env
LOG_LEVEL=INFO
API_RELOAD=false
API_KEY_ENABLED=true
CORS_ORIGINS=https://yourdomain.com
```

---

## 🏃 Running the API

### Development Mode

```bash
# Using the run script
python run.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# With multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or use the run script (configured via .env)
python run.py
```

### Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🔌 API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check API health and model status

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

### 2. Text Summarization

**Endpoint:** `POST /api/v1/summarize`

**Description:** Generate summary from medical report text

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Patient presents with fever and cough. Temperature 101°F. Prescribed antibiotics.",
    "max_length": 512,
    "temperature": 0.7
  }'
```

**Parameters:**
- `text` (required): Medical report text to summarize
- `max_length` (optional): Maximum length of summary (50-2048, default: 512)
- `temperature` (optional): Sampling temperature (0.1-1.0, default: 0.7)

**Response:**
```json
{
  "summary": "Patient has fever (101°F) and cough. Antibiotics prescribed.",
  "input_length": 75,
  "summary_length": 52
}
```

---

### 3. Question Answering

**Endpoint:** `POST /api/v1/analyze`

**Description:** Answer questions about medical reports

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Patient presents with fever and cough. Temperature 101°F.",
    "question": "What is the patient'\''s temperature?",
    "temperature": 0.7
  }'
```

**Response:**
```json
{
  "answer": "The patient's temperature is 101°F.",
  "question": "What is the patient's temperature?",
  "confidence": 0.95
}
```

---

### 4. Document Upload

**Endpoint:** `POST /api/v1/upload/document`

**Description:** Upload and process PDF or text documents

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload/document" \
  -F "file=@medical_report.pdf"
```

**Supported Formats:** PDF, TXT

**Response:**
```json
{
  "processed": true,
  "filename": "medical_report.pdf",
  "text_length": 1523,
  "message": "Document processed and added to vector store"
}
```

---

### 5. Image Upload

**Endpoint:** `POST /api/v1/upload/image`

**Description:** Upload and process medical images with OCR

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload/image" \
  -F "file=@xray_report.jpg"
```

**Supported Formats:** JPG, JPEG, PNG, TIFF

**Response:**
```json
{
  "processed": true,
  "filename": "xray_report.jpg",
  "extracted_text": "X-Ray Report: No abnormalities detected...",
  "text_length": 245
}
```

---

### 6. RAG Summarization

**Endpoint:** `POST /api/v1/rag/summarize`

**Description:** Generate summary using RAG for large documents

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/rag/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "max_length": 512,
    "temperature": 0.7,
    "top_k": 5
  }'
```

**Response:**
```json
{
  "summary": "Comprehensive summary of all documents in vector store...",
  "chunks_used": 5,
  "summary_length": 487
}
```

---

### 7. RAG Question Answering

**Endpoint:** `POST /api/v1/rag/question`

**Description:** Answer questions using RAG retrieval

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/rag/question" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main findings?",
    "top_k": 5,
    "temperature": 0.7
  }'
```

**Response:**
```json
{
  "answer": "The main findings include...",
  "question": "What are the main findings?",
  "relevant_chunks": ["chunk1", "chunk2"],
  "confidence": 0.92
}
```

---

## 💡 Usage Examples

### Python Example - Text Summarization

```python
import requests

url = "http://localhost:8000/api/v1/summarize"
payload = {
    "text": "Patient presents with fever and cough. Temperature 101°F. Prescribed antibiotics.",
    "temperature": 0.7
}

response = requests.post(url, json=payload)
print(response.json())
```

### Python Example - Question Answering

```python
import requests

url = "http://localhost:8000/api/v1/analyze"
payload = {
    "text": "Patient presents with fever and cough. Temperature 101°F.",
    "question": "What is the patient's temperature?"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Python Example - Document Upload

```python
import requests

url = "http://localhost:8000/api/v1/upload/document"
files = {"file": open("medical_report.pdf", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### Python Example - RAG Question

```python
import requests

# First upload a document
url_upload = "http://localhost:8000/api/v1/upload/document"
files = {"file": open("medical_report.pdf", "rb")}
requests.post(url_upload, files=files)

# Then query it
url_query = "http://localhost:8000/api/v1/rag/question"
payload = {
    "question": "What are the main findings?",
    "top_k": 5
}

response = requests.post(url_query, json=payload)
print(response.json())
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t medical-report-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/vector_store:/app/vector_store \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  --name medical-api \
  medical-report-api

# View logs
docker logs -f medical-api

# Stop container
docker stop medical-api
```

### GPU Support in Docker

Ensure NVIDIA Container Toolkit is installed:

```bash
# Install NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Run with GPU
docker run -d \
  --gpus all \
  -p 8000:8000 \
  --env-file .env \
  medical-report-api
```

---

## 📁 Project Structure

```
hack-nagpur/
│
├── app/                          # Main application code
│   ├── api/                      # API routes and endpoints
│   │   └── routes.py            # All API endpoints (7 endpoints)
│   ├── models/                   # Model management
│   │   └── model_loader.py      # MedGemma model loader
│   ├── processors/               # Document/image processing
│   │   ├── document_processor.py
│   │   └── image_processor.py
│   ├── rag/                      # RAG implementation
│   │   ├── vector_store.py      # Vector store management
│   │   └── rag_pipeline.py      # RAG pipeline
│   ├── schemas/                  # Request/response models
│   │   ├── requests.py
│   │   └── responses.py
│   ├── utils/                    # Utilities
│   │   └── logger.py            # Logging configuration
│   ├── config.py                # Configuration management
│   └── main.py                  # FastAPI application
│
├── tests/                        # Test suite
│   ├── test_api.py              # API endpoint tests
│   └── test_processors.py       # Processor tests
│
├── examples/                     # Usage examples
│   └── example_usage.py         # Example scripts
│
├── scripts/                      # Setup scripts
│   ├── setup.sh                 # Linux/Mac setup
│   └── setup.ps1                # Windows setup
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose setup
├── pytest.ini                    # Pytest configuration
├── Makefile                      # Common commands
├── setup.py                      # Package setup
└── run.py                        # Application entry point
```

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | >=0.109.0 |
| **ML Framework** | PyTorch | >=2.0.0 |
| **Transformers** | Hugging Face Transformers | >=4.37.0 |
| **Model** | Google MedGemma | 2B parameters |
| **Vector Store** | ChromaDB | >=0.4.0 |
| **Embeddings** | Sentence Transformers | >=2.3.0 |
| **Document Processing** | PyPDF | >=4.0.0 |
| **Image Processing** | Pillow | >=10.0.0 |
| **Logging** | Loguru | >=0.7.0 |
| **Configuration** | Pydantic Settings | >=2.1.0 |
| **Testing** | Pytest | >=7.4.0 |
| **Deployment** | Docker, Docker Compose | Latest |

---

## 💻 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::test_health_check -v
```

### Code Formatting

```bash
# Format code with black (if installed)
black app/ tests/

# Check formatting
black --check app/ tests/
```

### Development Workflow

1. **Make changes** to code
2. **Run tests** with pytest
3. **Test manually** using interactive docs
4. **Check logs** for any issues
5. **Commit** changes

---

## 🧪 Testing

### Manual Testing

Use the interactive API documentation:

1. Start the API: `python run.py`
2. Open browser: http://localhost:8000/docs
3. Try different endpoints
4. Check responses

### Example Test Script

```python
import requests

# Test health endpoint
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test summarization
response = requests.post(
    "http://localhost:8000/api/v1/summarize",
    json={
        "text": "Patient presents with fever and cough.",
        "temperature": 0.7
    }
)
print(response.json())
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: Model download is slow
**Solution:** First run downloads the model (~2-4GB). Be patient or use a pre-downloaded model.

#### Issue: Out of memory
**Solutions:**
- Use CPU mode: `MODEL_DEVICE=cpu`
- Enable quantization: `MODEL_QUANTIZATION=4bit`
- Reduce max length: `MAX_MODEL_LENGTH=1024`

#### Issue: CUDA not available
**Solutions:**
- Check CUDA installation: `nvidia-smi`
- Install CUDA toolkit
- Or use CPU mode: `MODEL_DEVICE=cpu`

#### Issue: Port 8000 already in use
**Solutions:**
- Change port in `.env`: `API_PORT=8001`
- Or kill process using port 8000

#### Issue: Dependencies installation fails
**Solutions:**
- Update pip: `pip install --upgrade pip`
- Use fresh virtual environment
- Install PyTorch separately first

### Debug Mode

Enable debug logging:

```env
LOG_LEVEL=DEBUG
```

Check logs:

```bash
tail -f logs/app.log
```

### Getting Help

1. Check logs: `tail -f logs/app.log`
2. Enable debug mode: `LOG_LEVEL=DEBUG`
3. Review this documentation
4. Check GitHub issues

---

## 🚀 Production Deployment

### Prerequisites

- Production server (Linux recommended)
- Python 3.9+
- (Optional) GPU with CUDA support
- Reverse proxy (Nginx/Apache)
- SSL certificate

### Deployment Steps

1. **Setup server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.9 python3-pip python3-venv -y
```

2. **Clone and setup**
```bash
git clone <repository-url>
cd hack-nagpur
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure for production**
```env
# .env
API_HOST=127.0.0.1
API_PORT=8000
API_WORKERS=4
API_RELOAD=false
LOG_LEVEL=INFO
API_KEY_ENABLED=true
API_KEY=your-secure-api-key
CORS_ORIGINS=https://yourdomain.com
```

4. **Run with systemd**

Create `/etc/systemd/system/medical-api.service`:

```ini
[Unit]
Description=Medical Report Analysis API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/hack-nagpur
Environment="PATH=/path/to/hack-nagpur/venv/bin"
ExecStart=/path/to/hack-nagpur/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable medical-api
sudo systemctl start medical-api
sudo systemctl status medical-api
```

5. **Setup Nginx reverse proxy**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. **Setup SSL with Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

---

## 📊 Performance Optimization

### GPU Acceleration

```env
MODEL_DEVICE=cuda
MODEL_QUANTIZATION=4bit
```

### Memory Optimization

```env
MODEL_QUANTIZATION=4bit
CHUNK_SIZE=256
MAX_MODEL_LENGTH=1024
```

### Scaling

- Use multiple workers: `API_WORKERS=4`
- Deploy multiple instances behind load balancer
- Use caching for frequently accessed data

---

## 🎯 Use Cases

1. **Medical Report Summarization** - Quickly summarize lengthy patient reports
2. **Clinical Decision Support** - Answer specific questions about patient data
3. **Medical Image Analysis** - Extract text from scanned reports
4. **Research and Analysis** - Batch process multiple reports
5. **EHR Integration** - Integrate with Electronic Health Record systems

---

## 📝 License

[Your License Here]

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request

---

## 📧 Support

For issues and questions:
- Check this documentation
- Review troubleshooting section
- Open an issue on GitHub

---

**Built with ❤️ for the future of healthcare AI**

#   P r i v a c y - S a f e - H e a l t h - R e c o r d - S u m m a r y - G e n e r a t o r  
 