# 🏥 MedGemma Patient Management System

> **A complete full-stack web application for medical report analysis and patient management using Google's MedGemma AI model.**

A production-grade **Patient Management System (PMS)** combining a modern React frontend with a powerful FastAPI backend. Designed for doctors and healthcare professionals to manage patients, upload medical reports, write prescriptions, and leverage AI-powered analysis for clinical decision support.

**Live Demo:** Frontend at `http://localhost:5173` | Backend API at `http://localhost:8000`

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Frontend Guide](#frontend-guide)
- [Backend API](#backend-api)
- [Database & Data](#database--data)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Development](#development)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)

---

## 📖 Project Overview

### What is MedGemma PMS?

A **complete Patient Management System** that brings AI-powered medical analysis to healthcare professionals:

- **👨‍⚕️ For Doctors**: Manage patient profiles, write prescriptions, upload medical reports, and get instant AI analysis
- **🤖 AI-Powered**: Uses Google's MedGemma 1.5 4B model for medical report summarization and image analysis
- **📱 Modern UI**: Beautiful, responsive React interface with real-time updates
- **🔒 Secure**: User authentication with role-based access (Admin, Doctor)
- **⚡ Fast**: Lazy-loaded AI model, optimized frontend with debouncing and memoization
- **📊 Complete**: Patient CRUD, prescription management, report uploads, AI analysis all in one place

### Key Workflows

1. **Login** → Select Patient → View Profile → Upload Report → AI Analyze → View Results
2. **Add Patient** → Create Prescriptions → Track Medical History → Generate Insights
3. **Upload Medical Images** → AI Vision Analysis → Extract Findings → Store in Database

---

## ✨ Features

### Frontend Features
- ✅ **Modern Dashboard** - Beautiful patient list with search and filtering
- ✅ **Patient Management** - Create, view, update patient profiles
- ✅ **Prescription Management** - Add and manage patient prescriptions with clinical notes
- ✅ **Report Upload** - Upload PDF, TXT, JPG, PNG medical reports
- ✅ **AI Analysis** - One-click AI analysis for both documents and images
- ✅ **Real-time Results** - View AI analysis results inline with loading states
- ✅ **Error Handling** - User-friendly error messages and validation
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile

### Backend Features
- ✅ **Patient CRUD API** - Full patient management endpoints
- ✅ **Medical Report Summarization** - AI-powered text summarization
- ✅ **Image Analysis** - Vision model for medical image analysis
- ✅ **Document Processing** - PDF and TXT text extraction
- ✅ **File Management** - Secure file upload and serving
- ✅ **User Authentication** - Login with role-based access control
- ✅ **Database** - SQLite with patient, prescription, and report tables
- ✅ **Lazy Model Loading** - AI model loads on first request (not on startup)

### Production Features
- ✅ **Type Safety** - Full TypeScript frontend + Pydantic backend
- ✅ **Error Handling** - Comprehensive exception handling and logging
- ✅ **API Documentation** - Interactive Swagger UI at `/docs`
- ✅ **Docker Support** - Easy deployment with Docker and Docker Compose
- ✅ **Testing** - Unit tests with pytest
- ✅ **Logging** - Structured logging with rotation
- ✅ **Configuration** - Environment-based configuration
- ✅ **GPU Acceleration** - CUDA support with automatic CPU fallback
- ✅ **Model Quantization** - 4-bit/8-bit quantization for memory efficiency

---

## 🚀 Quick Start

Get the full application running in 5 minutes!

### Prerequisites
- **Python 3.9+** installed
- **Node.js 18+** installed (for frontend)
- **npm** or **yarn** (comes with Node.js)
- At least **8GB RAM**
- At least **10GB disk space** (for AI model)
- (Optional) CUDA-capable GPU for faster AI inference

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
# 1. Backend setup
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
mkdir models vector_store logs

# 2. Frontend setup
cd frontend/doctorms
npm install
cd ../..
```

### Run the Application

**Terminal 1 - Backend (FastAPI):**
```bash
python run.py
# Backend starts at http://localhost:8000
```

**Terminal 2 - Frontend (React + Vite):**
```bash
cd frontend/doctorms
npm run dev
# Frontend starts at http://localhost:5173
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |
| `doctor` | `doctor123` | Doctor |
| `drsmith` | `smith123` | Doctor |

---

## 📦 Installation

### Step-by-Step Installation

#### Backend Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd medgemma-pms

# 2. Create Python virtual environment
python -m venv venv

# Activate (Windows):
venv\Scripts\activate

# Activate (Linux/Mac):
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Setup environment configuration
cp .env.example .env

# 5. Create necessary directories
mkdir -p models vector_store logs data/uploads
```

#### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend/doctorms

# 2. Install Node dependencies
npm install

# 3. Return to root
cd ../..
```

### Verify Installation

```bash
# Test backend
python -c "import fastapi; print('✓ FastAPI installed')"

# Test frontend
cd frontend/doctorms && npm list react && cd ../..
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

## 🏃 Running the Application

### Development Mode (Recommended)

**Terminal 1 - Start Backend:**
```bash
# Activate virtual environment first
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

python run.py
# Backend runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend/doctorms
npm run dev
# Frontend runs at http://localhost:5173
# Hot reload enabled - changes appear instantly
```

### Production Mode

```bash
# Backend with multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend build
cd frontend/doctorms
npm run build
# Creates optimized build in dist/
```

### Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | Patient Management UI |
| **Backend API** | http://localhost:8000 | REST API endpoints |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| **Health Check** | http://localhost:8000/health | API status |

---

## 🎨 Frontend Guide

### User Interface Overview

#### Login Page
- Clean, modern login form
- Default credentials: `doctor/doctor123`
- Role-based access (Admin/Doctor)

#### Dashboard
- **Patient List** - Search and filter patients
- **Add Patient** - Create new patient profiles
- **Quick Stats** - Total patients, recent activity
- **Patient Cards** - Click to view full profile

#### Patient Details
Four main tabs:

1. **Overview** - Patient info, age, gender, medical history
2. **Prescriptions** - Add/view prescriptions with clinical notes
3. **Reports** - Upload and manage medical reports
4. **AI Analysis** - View AI-generated insights

#### Reports Tab Features
- **Upload** - Drag-drop or click to upload PDF, TXT, JPG, PNG
- **AI Analyze** - One-click AI analysis button
- **Download** - Download uploaded files
- **Results** - View AI analysis inline with findings

### Frontend Technology
- **React 19** - Modern UI framework
- **TypeScript** - Type-safe code
- **Vite** - Lightning-fast dev server
- **CSS Variables** - Consistent theming
- **Responsive Design** - Mobile-friendly

---

## 🔌 Backend API Endpoints

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
  "model_loaded": false,
  "version": "1.0.0"
}
```

---

### 2. Patient Management

**Endpoints:**
- `POST /login` - User login
- `GET /patients` - List all patients
- `POST /patients` - Create new patient
- `GET /patients/{id}` - Get patient details
- `PUT /patients/{id}` - Update patient
- `DELETE /patients/{id}` - Delete patient

**Example - Create Patient:**
```bash
curl -X POST "http://localhost:8000/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 45,
    "gender": "M"
  }'
```

---

### 3. Text Summarization

**Endpoint:** `POST /api/v1/summarize`

**Description:** Generate summary from medical report text

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Patient presents with fever and cough. Temperature 101°F. Prescribed antibiotics."
  }'
```

**Response:**
```json
{
  "summary": "Patient has fever (101°F) and cough. Antibiotics prescribed."
}
```

---

### 4. Image Analysis

**Endpoint:** `POST /api/v1/analyze/image`

**Description:** Analyze medical images (X-rays, scans, etc.)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/image" \
  -F "file=@xray.jpg" \
  -F "query=Analyze this X-ray image"
```

**Supported Formats:** JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP

**Response:**
```json
{
  "analysis": "X-ray shows normal findings with no abnormalities detected...",
  "filename": "xray.jpg"
}
```

---

### 5. Report Management

**Endpoints:**
- `POST /reports` - Upload medical report
- `GET /reports/{patient_id}` - Get patient's reports
- `GET /files/{filename}` - Download report file
- `GET /reports/{filename}/extract-text` - Extract text from PDF/TXT

**Example - Upload Report:**
```bash
curl -X POST "http://localhost:8000/reports" \
  -F "file=@report.pdf" \
  -F "patient_id=1" \
  -F "title=Blood Test Report" \
  -F "doctor_name=Dr. Smith"
```

---

### 6. Prescription Management

**Endpoints:**
- `POST /prescriptions` - Add prescription
- `GET /prescriptions/{patient_id}` - Get patient's prescriptions
- `PUT /prescriptions/{id}` - Update prescription
- `DELETE /prescriptions/{id}` - Delete prescription

**Example - Add Prescription:**
```bash
curl -X POST "http://localhost:8000/prescriptions" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_name": "Dr. Smith",
    "diagnosis": "Type 2 Diabetes",
    "medicines": [
      {"name": "Metformin", "dose": "500mg", "frequency": "Twice daily"}
    ],
    "notes": "Monitor blood glucose levels"
  }'
```

---

## 💡 Usage Examples

### Frontend Usage - Patient Workflow

1. **Login**
```
URL: http://localhost:5173
Username: doctor
Password: doctor123
```

2. **View Patients**
- Dashboard shows all patients
- Search by name
- Click patient to view details

3. **Upload Report**
- Go to Reports tab
- Click "Upload Report"
- Select PDF, TXT, JPG, or PNG file
- Fill in title and doctor name
- Click "Upload"

4. **AI Analyze**
- Click "🧠 AI Analyze" button on any report
- Wait for AI to process
- View results inline

### Backend Usage - Python Examples

**Example 1 - Login and Get Patients**
```python
import requests

# Login
response = requests.post("http://localhost:8000/login", json={
    "username": "doctor",
    "password": "doctor123"
})
token = response.json()["access_token"]

# Get patients
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/patients", headers=headers)
print(response.json())
```

**Example 2 - Upload and Analyze Report**
```python
import requests

# Upload report
with open("report.pdf", "rb") as f:
    files = {"file": f}
    data = {
        "patient_id": 1,
        "title": "Blood Test",
        "doctor_name": "Dr. Smith"
    }
    response = requests.post(
        "http://localhost:8000/reports",
        files=files,
        data=data
    )
    report = response.json()

# Analyze with AI
response = requests.post("http://localhost:8000/api/v1/summarize", json={
    "text": "Patient blood test shows elevated glucose levels..."
})
print(response.json())
```

**Example 3 - Add Prescription**
```python
import requests

response = requests.post("http://localhost:8000/prescriptions", json={
    "patient_id": 1,
    "doctor_name": "Dr. Smith",
    "diagnosis": "Type 2 Diabetes",
    "medicines": [
        {"name": "Metformin", "dose": "500mg", "frequency": "Twice daily"}
    ],
    "notes": "Monitor blood glucose"
})
print(response.json())
```

---

## 📊 Database & Data

### Database Schema

**Users Table**
```
id | username | password | role
```

**Patients Table**
```
id | name | age | gender | created_at
```

**Prescriptions Table**
```
id | patient_id | doctor_name | diagnosis | medicines (JSON) | notes | created_at
```

**Reports Table**
```
id | patient_id | doctor_name | title | file_path | created_at
```

### Sample Data

The project includes a seed script to populate sample data:

```bash
python scripts/seed_patients.py
```

This creates 5 realistic patient profiles with:
- Patient information (name, age, gender)
- Medical conditions and prescriptions
- Sample medical reports (PDF/TXT files)

### File Storage

- **Database**: `data/pms.db` (SQLite)
- **Uploads**: `data/uploads/` (PDF, TXT, JPG, PNG files)
- **Models**: `models/` (AI model cache)
- **Logs**: `logs/` (application logs)

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start both frontend and backend
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Rebuild images
docker-compose up -d --build
```

### Using Docker Directly

**Build image:**
```bash
docker build -t medgemma-pms .
```

**Run container:**
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  --name medgemma-backend \
  medgemma-pms
```

**View logs:**
```bash
docker logs -f medgemma-backend
```

**Stop container:**
```bash
docker stop medgemma-backend
docker rm medgemma-backend
```

### GPU Support in Docker

**Install NVIDIA Container Toolkit:**
```bash
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

**Run with GPU:**
```bash
docker run -d \
  --gpus all \
  -p 8000:8000 \
  --env-file .env \
  medgemma-pms
```

### Docker Compose with GPU

Update `docker-compose.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## 📁 Project Structure

```
medgemma-pms/
│
├── 📂 app/                           # FastAPI Backend
│   ├── api/
│   │   ├── patients.py              # Patient, prescription, report CRUD
│   │   └── routes.py                # AI analysis endpoints
│   ├── models/
│   │   └── model_loader.py          # MedGemma model management
│   ├── processors/
│   │   ├── document_processor.py    # PDF/TXT text extraction
│   │   └── image_processor.py       # Image processing & analysis
│   ├── rag/
│   │   ├── vector_store.py          # Vector store (ChromaDB)
│   │   └── rag_pipeline.py          # RAG pipeline
│   ├── schemas/
│   │   ├── requests.py              # Request models
│   │   └── responses.py             # Response models
│   ├── utils/
│   │   └── logger.py                # Logging setup
│   ├── config.py                    # Configuration
│   ├── database.py                  # SQLite schema & init
│   └── main.py                      # FastAPI app factory
│
├── 📂 frontend/doctorms/             # React + TypeScript Frontend
│   ├── src/
│   │   ├── App.tsx                  # Main dashboard component
│   │   ├── Login.tsx                # Login page
│   │   ├── PatientDetails.tsx       # Patient profile with tabs
│   │   ├── PrescriptionsTab.tsx     # Prescription management
│   │   ├── ReportsTab.tsx           # Report upload & AI analysis
│   │   ├── components/              # Reusable components
│   │   ├── App.css                  # Component styles
│   │   └── index.css                # Global styles & CSS variables
│   ├── vite.config.ts               # Vite configuration with proxy
│   ├── tsconfig.json                # TypeScript config
│   ├── package.json                 # Node dependencies
│   └── index.html                   # HTML entry point
│
├── 📂 scripts/                       # Utility Scripts
│   ├── seed_patients.py             # Populate sample data
│   ├── test_sample.py               # API smoke tests
│   ├── setup.sh                     # Linux/Mac setup
│   └── setup.ps1                    # Windows setup
│
├── 📂 tests/                        # Test Suite
│   ├── test_api.py                  # API tests
│   └── test_processors.py           # Processor tests
│
├── 📂 examples/                     # Usage Examples
│   └── example_usage.py             # API usage examples
│
├── 📂 data/                         # Runtime Data (git-ignored)
│   ├── pms.db                       # SQLite database
│   └── uploads/                     # Uploaded files
│
├── 📂 models/                       # AI Model Cache (git-ignored)
│   └── medgemma-1.5-4b/             # Downloaded model
│
├── 📂 logs/                         # Application Logs (git-ignored)
│   └── app.log
│
├── README.md                        # This file
├── DESIGN.md                        # Architecture & design doc
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── Dockerfile                       # Docker image
├── docker-compose.yml               # Docker Compose setup
├── Makefile                         # Common commands
├── pytest.ini                       # Pytest config
├── setup.py                         # Package setup
└── run.py                           # Backend entry point
```

---

## 🛠️ Technology Stack

### Frontend
| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | React | 19.2.0 |
| **Language** | TypeScript | 5.x |
| **Build Tool** | Vite | 7.2.4 |
| **Styling** | CSS Variables | Native |
| **HTTP Client** | Fetch API | Native |
| **State Management** | React Hooks | Native |

### Backend
| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | >=0.109.0 |
| **Server** | Uvicorn | >=0.27.0 |
| **Database** | SQLite | 3.x |
| **ORM** | sqlite3 | Native |
| **ML Framework** | PyTorch | >=2.0.0 |
| **Transformers** | Hugging Face | >=4.37.0 |
| **AI Model** | Google MedGemma 1.5 4B | 4B params |
| **Vector Store** | ChromaDB | >=0.4.0 |
| **Embeddings** | Sentence Transformers | >=2.3.0 |
| **Document Processing** | PyPDF | >=4.0.0 |
| **Image Processing** | Pillow | >=10.0.0 |
| **Logging** | Loguru | >=0.7.0 |
| **Validation** | Pydantic | >=2.1.0 |
| **Testing** | Pytest | >=7.4.0 |

### DevOps
| Component | Technology |
|-----------|-----------|
| **Containerization** | Docker |
| **Orchestration** | Docker Compose |
| **Version Control** | Git |

---

## 💻 Development

### Backend Development

**Run in development mode with auto-reload:**
```bash
python run.py
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Run tests:**
```bash
# All tests
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/test_api.py::test_health_check -v
```

### Frontend Development

**Run dev server with hot reload:**
```bash
cd frontend/doctorms
npm run dev
```

**Build for production:**
```bash
npm run build
```

**Type checking:**
```bash
npm run type-check
```

### Development Workflow

1. **Backend changes** → Tests pass → Check API docs
2. **Frontend changes** → Hot reload → Check browser
3. **Database changes** → Reset DB → Seed sample data
4. **Both changes** → Run both servers → Test full workflow
5. **Commit** → Push to GitHub

### Useful Commands

```bash
# Seed sample data
python scripts/seed_patients.py

# Run API smoke tests
python scripts/test_sample.py

# Check backend syntax
python -m py_compile app/api/patients.py

# Check frontend types
cd frontend/doctorms && npm run type-check
```

---

## 🧪 Testing

### Manual Testing - Frontend

1. Start both servers (backend + frontend)
2. Open http://localhost:5173
3. Login with `doctor/doctor123`
4. Test workflows:
   - View patient list
   - Click patient to view details
   - Upload a report
   - Click "AI Analyze"
   - Add a prescription
   - Check error handling

### Manual Testing - Backend API

Use the interactive Swagger UI:

1. Start backend: `python run.py`
2. Open http://localhost:8000/docs
3. Try endpoints:
   - `GET /health` - Check API status
   - `POST /login` - Test authentication
   - `GET /patients` - List patients
   - `POST /api/v1/summarize` - Test AI

### Automated Testing

```bash
# Run all backend tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Test Coverage

- API endpoints (login, patients, reports, prescriptions)
- Document processing (PDF, TXT extraction)
- Image processing (JPG, PNG handling)
- Error handling and validation

---

## 🔧 Troubleshooting

### Frontend Issues

#### Issue: Frontend won't start
```bash
# Clear node_modules and reinstall
cd frontend/doctorms
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### Issue: API calls failing (CORS error)
- Ensure backend is running on `localhost:8000`
- Check Vite proxy config in `vite.config.ts`
- Verify `.env` has correct API URL

#### Issue: Login not working
- Check default credentials: `doctor/doctor123`
- Verify database exists: `data/pms.db`
- Check backend logs for errors

#### Issue: File upload fails
- Ensure `data/uploads/` directory exists
- Check file size (max 50MB)
- Verify file format (PDF, TXT, JPG, PNG)

### Backend Issues

#### Issue: Model download is slow
- First run downloads model (~2-4GB)
- Be patient or use pre-downloaded model
- Check internet connection

#### Issue: Out of memory
```env
MODEL_DEVICE=cpu
MODEL_QUANTIZATION=4bit
MAX_MODEL_LENGTH=1024
```

#### Issue: Port 8000 already in use
```bash
# Change port in .env
API_PORT=8001

# Or kill process using port 8000
# Windows: netstat -ano | findstr :8000
# Linux: lsof -i :8000
```

#### Issue: Database locked
```bash
# Remove old database and reseed
rm data/pms.db
python scripts/seed_patients.py
```

#### Issue: Dependencies fail to install
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

**Enable debug logging:**
```env
LOG_LEVEL=DEBUG
```

**Check logs:**
```bash
# Backend logs
tail -f logs/app.log

# Frontend console
# Open browser DevTools (F12) → Console tab
```

**Test API health:**
```bash
curl http://localhost:8000/health
```

### Getting Help

1. Check logs (backend and browser console)
2. Enable debug mode
3. Review this documentation
4. Check DESIGN.md for architecture details
5. Open GitHub issue with logs

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

#
