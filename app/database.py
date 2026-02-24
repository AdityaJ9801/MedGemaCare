"""SQLite database for Patient Management System."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path("./data/pms.db")
UPLOAD_DIR = Path("./data/uploads")


def get_db() -> sqlite3.Connection:
    """Get a SQLite connection with row factory enabled."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables and seed default users if they don't exist."""
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    UNIQUE NOT NULL,
            password TEXT    NOT NULL,
            role     TEXT    NOT NULL CHECK(role IN ('ADMIN','DOCTOR'))
        );

        CREATE TABLE IF NOT EXISTS patients (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            age        INTEGER NOT NULL,
            gender     TEXT    NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS prescriptions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id  INTEGER NOT NULL,
            doctor_name TEXT    NOT NULL,
            diagnosis   TEXT    NOT NULL,
            medicines   TEXT    NOT NULL,
            notes       TEXT    DEFAULT '',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );

        CREATE TABLE IF NOT EXISTS reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id  INTEGER NOT NULL,
            doctor_name TEXT    NOT NULL,
            title       TEXT    NOT NULL,
            file_path   TEXT    NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
    """)

    # Seed default credentials (plain-text for demo – swap for hashing in production)
    for username, password, role in [
        ("admin",   "admin123",  "ADMIN"),
        ("doctor",  "doctor123", "DOCTOR"),
        ("drsmith", "smith123",  "DOCTOR"),
    ]:
        cur.execute(
            "INSERT OR IGNORE INTO users (username, password, role) VALUES (?,?,?)",
            (username, password, role),
        )

    conn.commit()
    conn.close()

