"""Patient Management System routes (auth, patients, prescriptions, reports)."""

import json
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.database import UPLOAD_DIR, get_db
from app.processors.document_processor import DocumentProcessor
from app.utils.logger import app_logger

patients_router = APIRouter()


# ── AUTH ──────────────────────────────────────────────────────────────────────

@patients_router.post("/login")
async def login(body: dict):
    username = body.get("username", "")
    password = body.get("password", "")
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": row["username"], "role": row["role"]}


# ── PATIENTS ──────────────────────────────────────────────────────────────────

@patients_router.get("/patients")
async def list_patients():
    conn = get_db()
    rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@patients_router.post("/patients")
async def create_patient(body: dict):
    name   = body.get("name")
    age    = body.get("age")
    gender = body.get("gender", "Male")
    if not name or not age:
        raise HTTPException(status_code=400, detail="name and age are required")
    conn   = get_db()
    cur    = conn.execute(
        "INSERT INTO patients (name, age, gender) VALUES (?,?,?)", (name, int(age), gender)
    )
    row    = conn.execute("SELECT * FROM patients WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.commit(); conn.close()
    return dict(row)


# ── PRESCRIPTIONS ─────────────────────────────────────────────────────────────

@patients_router.get("/patients/{patient_id}/prescriptions")
async def list_prescriptions(patient_id: int):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM prescriptions WHERE patient_id=? ORDER BY created_at DESC", (patient_id,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        item = dict(r)
        item["medicines"] = json.loads(item["medicines"])
        result.append(item)
    return result


@patients_router.post("/prescriptions")
async def create_prescription(body: dict):
    patient_id  = body.get("patient_id")
    doctor_name = body.get("doctor_name")
    diagnosis   = body.get("diagnosis")
    medicines   = body.get("medicines", [])
    notes       = body.get("notes", "")
    conn = get_db()
    cur  = conn.execute(
        "INSERT INTO prescriptions (patient_id, doctor_name, diagnosis, medicines, notes)"
        " VALUES (?,?,?,?,?)",
        (patient_id, doctor_name, diagnosis, json.dumps(medicines), notes),
    )
    row  = conn.execute("SELECT * FROM prescriptions WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.commit(); conn.close()
    item = dict(row)
    item["medicines"] = json.loads(item["medicines"])
    return item


# ── REPORTS ───────────────────────────────────────────────────────────────────

@patients_router.get("/patients/{patient_id}/reports")
async def list_reports(patient_id: int):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reports WHERE patient_id=? ORDER BY created_at DESC", (patient_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@patients_router.post("/reports")
async def upload_report(
    patient_id:  int        = Form(...),
    doctor_name: str        = Form(...),
    title:       str        = Form(...),
    file:        UploadFile = File(...),
):
    try:
        content  = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")

        filename = f"{patient_id}_{file.filename}"
        dest     = UPLOAD_DIR / filename
        dest.write_bytes(content)
        app_logger.info(f"Report saved: {dest}")

        conn = get_db()
        cur  = conn.execute(
            "INSERT INTO reports (patient_id, doctor_name, title, file_path) VALUES (?,?,?,?)",
            (patient_id, doctor_name, title, filename),  # Store only filename, not full path
        )
        row  = conn.execute("SELECT * FROM reports WHERE id=?", (cur.lastrowid,)).fetchone()
        conn.commit(); conn.close()
        return dict(row)
    except Exception as e:
        app_logger.error(f"Error uploading report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ── FILE SERVING ──────────────────────────────────────────────────────────────

@patients_router.get("/files/{filename}")
async def serve_file(filename: str):
    path = UPLOAD_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(path))


@patients_router.get("/reports/{filename}/extract-text")
async def extract_report_text(filename: str):
    """Extract text content from a report file (PDF, TXT, etc.)."""
    try:
        path = UPLOAD_DIR / filename
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        # Extract text based on file type
        text = DocumentProcessor.process_document(str(path))

        return {
            "filename": filename,
            "text": text,
            "length": len(text)
        }
    except ValueError as e:
        app_logger.error(f"Error extracting text from {filename}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        app_logger.error(f"Error extracting text from {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

