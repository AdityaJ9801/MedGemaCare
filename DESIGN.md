# System Design — MedGemma Patient Management System

## Overview

A full-stack medical AI platform that combines a **FastAPI** backend powered by **Google MedGemma 1.5 4B** with a **React + TypeScript** frontend. The system enables doctors to manage patients, upload medical reports, write prescriptions, and get AI-driven clinical analysis on documents and images.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Browser (React)                       │
│  Login → Dashboard → Patient Details → Reports/Rx → AI   │
└───────────────────────┬──────────────────────────────────┘
                        │  HTTP (Vite proxy → :8000)
┌───────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend (:8000)                   │
│                                                           │
│  /login  /patients  /prescriptions  /reports  /files     │
│  /api/v1/summarize  /analyze/image  /analyze/ehr  …      │
│                                                           │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  SQLite DB  │  │ data/uploads │  │  MedGemma Model │  │
│  │  (pms.db)   │  │  (files)     │  │  (lazy-loaded)  │  │
│  └─────────────┘  └──────────────┘  └─────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
.
├── app/                        # FastAPI application
│   ├── api/
│   │   ├── patients.py         # Patient, prescription & report CRUD + file serving
│   │   └── routes.py           # AI inference endpoints (summarize, image, EHR, RAG)
│   ├── models/
│   │   └── model_loader.py     # MedGemma loader with lazy-init & quantization
│   ├── processors/
│   │   ├── document_processor.py  # PDF / TXT text extraction (PyPDF)
│   │   └── image_processor.py     # Image loading (PIL, DICOM, NIfTI)
│   ├── rag/                    # Retrieval-Augmented Generation pipeline
│   ├── schemas/                # Pydantic request/response models
│   ├── utils/                  # Logger, helpers
│   ├── config.py               # App settings (model path, limits, formats)
│   ├── database.py             # SQLite init, table schema, seed users
│   └── main.py                 # App factory, CORS, startup hook
│
├── frontend/doctorms/          # React + TypeScript + Vite SPA
│   └── src/
│       ├── App.tsx             # Dashboard, patient list, add-patient modal
│       ├── Login.tsx           # Auth page
│       ├── PatientDetails.tsx  # Profile with tabs (Overview / Rx / Reports / AI)
│       ├── PrescriptionsTab.tsx
│       ├── ReportsTab.tsx      # Upload, view, AI-analyse reports
│       ├── App.css             # Component styles
│       └── index.css           # CSS variables & global design system
│
├── scripts/
│   ├── seed_patients.py        # Populate DB with sample patient profiles
│   ├── test_sample.py          # Quick API smoke-test script
│   ├── setup.sh                # Linux/macOS dev setup
│   └── setup.ps1               # Windows dev setup
│
├── tests/                      # Pytest test suite
├── examples/                   # API usage examples
├── run.py                      # Uvicorn entry point
├── ui.py                       # Optional Gradio debug UI
├── Dockerfile / docker-compose.yml
├── Makefile                    # Common dev commands
└── requirements.txt
```

---

## Key Design Decisions

### 1. Lazy Model Loading
MedGemma (4 B params) is **not** loaded at startup. It loads on the first AI request via `_ensure_model()`. This keeps the API responsive immediately and avoids OOM errors on machines without a GPU.

### 2. File-type–aware AI Routing
The frontend detects file extension before calling AI:
- **PDF / TXT** → `GET /reports/{file}/extract-text` → `POST /api/v1/summarize`
- **JPG / PNG / etc.** → fetch blob → `POST /api/v1/analyze/image` (vision model)

### 3. Filename-only Storage
The database stores **only the filename** (e.g. `3_report.pdf`), never the full path. The backend reconstructs the full path as `data/uploads/{filename}` at serve time.

### 4. Vite Proxy
All frontend API calls use **relative URLs** (`/patients`, `/api/v1/summarize`). Vite's dev-server proxy forwards them to `localhost:8000`, so no CORS issues during development and no URL changes are needed for production.

---

## Data Model

```
users         (id, username, password, role)
patients      (id, name, age, gender, created_at)
prescriptions (id, patient_id, doctor_name, diagnosis, medicines JSON, notes, created_at)
reports       (id, patient_id, doctor_name, title, file_path, created_at)
```

---

## AI Endpoints

| Endpoint | Input | Output |
|----------|-------|--------|
| `POST /api/v1/summarize` | `{ text }` | Clinical summary |
| `POST /api/v1/analyze` | `{ text, question }` | Q&A answer |
| `POST /api/v1/analyze/image` | multipart image file | Visual analysis |
| `POST /api/v1/analyze/ehr` | `{ ehr_text }` | EHR insights |
| `POST /api/v1/extract/lab` | `{ text }` | Structured lab JSON |
| `POST /api/v1/rag/summarize` | `{ query }` | RAG summary |
| `GET  /reports/{file}/extract-text` | filename | Extracted plain text |

---

## Default Credentials (Demo)

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | ADMIN |
| `doctor` | `doctor123` | DOCTOR |
| `drsmith` | `smith123` | DOCTOR |

