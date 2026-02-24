"""Seed 5 realistic sample patient profiles with prescriptions and reports."""

import json
import sqlite3
from pathlib import Path

DB_PATH    = Path("./data/pms.db")
UPLOAD_DIR = Path("./data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ── Sample Data ────────────────────────────────────────────────────────────────

PATIENTS = [
    {"name": "Aarav Mehta",    "age": 45, "gender": "Male"},
    {"name": "Priya Sharma",   "age": 32, "gender": "Female"},
    {"name": "Rohan Desai",    "age": 60, "gender": "Male"},
    {"name": "Sneha Patil",    "age": 28, "gender": "Female"},
    {"name": "Vikram Nair",    "age": 52, "gender": "Male"},
]

PRESCRIPTIONS = {
    "Aarav Mehta": [
        {
            "doctor_name": "Dr. Anjali Rao",
            "diagnosis":   "Type 2 Diabetes Mellitus with hypertension",
            "medicines":   ["Metformin 500mg – twice daily after meals",
                            "Amlodipine 5mg – once daily in the morning",
                            "Aspirin 75mg – once daily after breakfast"],
            "notes":       "Monitor blood glucose daily. Avoid sugary foods. Follow-up in 4 weeks.",
        },
        {
            "doctor_name": "Dr. Suresh Kumar",
            "diagnosis":   "Hyperlipidaemia",
            "medicines":   ["Atorvastatin 20mg – once daily at night"],
            "notes":       "Lipid profile to be repeated after 3 months. Low-fat diet advised.",
        },
    ],
    "Priya Sharma": [
        {
            "doctor_name": "Dr. Meena Iyer",
            "diagnosis":   "Iron-deficiency anaemia",
            "medicines":   ["Ferrous sulphate 200mg – once daily",
                            "Folic acid 5mg – once daily",
                            "Vitamin C 500mg – once daily"],
            "notes":       "Take iron tablets on empty stomach. Avoid tea/coffee 1 hour before/after.",
        },
        {
            "doctor_name": "Dr. Meena Iyer",
            "diagnosis":   "Migraine with aura",
            "medicines":   ["Sumatriptan 50mg – at onset of attack (max 2/day)",
                            "Propranolol 40mg – twice daily (prophylaxis)"],
            "notes":       "Keep headache diary. Avoid known triggers (stress, caffeine withdrawal).",
        },
    ],
    "Rohan Desai": [
        {
            "doctor_name": "Dr. Prakash Joshi",
            "diagnosis":   "Chronic Obstructive Pulmonary Disease (COPD) – Stage II",
            "medicines":   ["Tiotropium inhaler 18mcg – once daily",
                            "Salbutamol inhaler 100mcg – as needed",
                            "Prednisolone 10mg – during exacerbations"],
            "notes":       "Absolute smoking cessation mandatory. Annual flu vaccination recommended.",
        },
        {
            "doctor_name": "Dr. Prakash Joshi",
            "diagnosis":   "Osteoarthritis – bilateral knees",
            "medicines":   ["Diclofenac 50mg – twice daily after meals",
                            "Pantoprazole 40mg – once daily (gastric protection)",
                            "Glucosamine 1500mg – once daily"],
            "notes":       "Physiotherapy 3×/week. Avoid prolonged standing. Weight management advised.",
        },
    ],
    "Sneha Patil": [
        {
            "doctor_name": "Dr. Anjali Rao",
            "diagnosis":   "Polycystic Ovary Syndrome (PCOS) with insulin resistance",
            "medicines":   ["Metformin 500mg – twice daily",
                            "Inositol 2g – once daily",
                            "Vitamin D3 60,000 IU – once weekly"],
            "notes":       "Regular exercise 30 min/day. Low-glycaemic-index diet. USG pelvis in 3 months.",
        },
    ],
    "Vikram Nair": [
        {
            "doctor_name": "Dr. Suresh Kumar",
            "diagnosis":   "Coronary Artery Disease – post PTCA (2023)",
            "medicines":   ["Clopidogrel 75mg – once daily",
                            "Aspirin 75mg – once daily",
                            "Rosuvastatin 40mg – once daily at night",
                            "Bisoprolol 5mg – once daily",
                            "Ramipril 5mg – once daily"],
            "notes":       "Strict cardiac diet. Avoid strenuous activity without consultation. Treadmill test in 6 months.",
        },
        {
            "doctor_name": "Dr. Suresh Kumar",
            "diagnosis":   "Hypothyroidism",
            "medicines":   ["Levothyroxine 50mcg – once daily on empty stomach"],
            "notes":       "Take 30 min before breakfast. TSH to be checked in 6 weeks.",
        },
    ],
}

REPORTS = {
    "Aarav Mehta": [
        ("Blood Glucose Report",         "HbA1c: 8.2% (High). Fasting glucose: 148 mg/dL. Post-prandial glucose: 210 mg/dL.\nImpression: Poor glycaemic control. Increase Metformin dose discussed.\nRecommendation: Dietary counselling, re-test in 3 months."),
        ("Lipid Profile Report",          "Total Cholesterol: 220 mg/dL. LDL: 145 mg/dL. HDL: 38 mg/dL. Triglycerides: 185 mg/dL.\nImpression: Borderline high LDL, low HDL. Statin therapy initiated.\nRecommendation: Repeat after 3 months of statin therapy."),
    ],
    "Priya Sharma": [
        ("Complete Blood Count (CBC)",    "Haemoglobin: 9.4 g/dL (Low). MCV: 68 fL (Low). MCH: 22 pg (Low). RBC: 3.8 million/µL.\nImpression: Microcytic hypochromic anaemia consistent with iron deficiency.\nRecommendation: Iron supplementation, dietary modification, follow-up CBC in 8 weeks."),
        ("MRI Brain Report",              "Sequences: T1, T2, FLAIR, DWI. No acute infarct or haemorrhage. White matter appears normal.\nImpression: No structural intracranial abnormality identified. Changes consistent with migraine without lesion.\nRecommendation: Clinical correlation. Prophylactic therapy recommended."),
    ],
    "Rohan Desai": [
        ("Spirometry / PFT Report",       "FEV1: 58% predicted. FVC: 72% predicted. FEV1/FVC ratio: 0.61.\nImpression: Obstructive pattern consistent with COPD Stage II (GOLD criteria).\nRecommendation: Continue bronchodilator therapy. Pulmonary rehabilitation program advised."),
        ("X-Ray Both Knees (AP & Lat)",   "Moderate joint space narrowing bilateral medial compartments. Osteophyte formation at tibial plateaus.\nImpression: Osteoarthritis bilateral knees, Grade III (Kellgren-Lawrence).\nRecommendation: Conservative management. Physiotherapy. Surgical review if no improvement in 6 months."),
    ],
    "Sneha Patil": [
        ("Ultrasound Pelvis Report",      "Uterus: Normal size and echotexture. Right ovary: 12 follicles <10mm (string-of-pearls sign). Left ovary: 10 follicles.\nImpression: Polycystic ovarian morphology bilaterally. No free fluid in POD.\nRecommendation: Hormonal profile correlation. Follow-up in 3 months."),
        ("Fasting Insulin & OGTT",        "Fasting insulin: 18 µIU/mL (High). HOMA-IR: 3.8 (Insulin resistant). Fasting glucose: 95 mg/dL. 2-hr OGTT: 142 mg/dL.\nImpression: Insulin resistance without overt diabetes. Consistent with PCOS-related metabolic syndrome.\nRecommendation: Lifestyle intervention, Metformin initiated."),
    ],
    "Vikram Nair": [
        ("2D Echo + Doppler Report",      "EF: 48% (Mildly reduced). LV diastolic dysfunction Grade I. Mild MR. No regional wall motion abnormality at rest.\nImpression: Ischaemic cardiomyopathy with mildly reduced EF post-PTCA. Diastolic dysfunction noted.\nRecommendation: Continue cardiac medications. Repeat echo in 6 months. Cardiac rehab advised."),
        ("Thyroid Function Test (TFT)",   "TSH: 7.8 mIU/L (High). Free T4: 0.72 ng/dL (Low-normal). Free T3: 2.9 pg/mL (Normal).\nImpression: Primary hypothyroidism. Subclinical to overt transition.\nRecommendation: Levothyroxine initiated. TSH recheck in 6 weeks."),
    ],
}

# ── Seed ──────────────────────────────────────────────────────────────────────

def seed():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    for p in PATIENTS:
        # Skip if patient already exists by name
        existing = conn.execute("SELECT id FROM patients WHERE name=?", (p["name"],)).fetchone()
        if existing:
            print(f"  [skip] {p['name']} already exists")
            continue

        cur = conn.execute(
            "INSERT INTO patients (name, age, gender) VALUES (?,?,?)",
            (p["name"], p["age"], p["gender"]),
        )
        pid = cur.lastrowid
        print(f"  [+] Patient: {p['name']} (id={pid})")

        for rx in PRESCRIPTIONS.get(p["name"], []):
            conn.execute(
                "INSERT INTO prescriptions (patient_id, doctor_name, diagnosis, medicines, notes)"
                " VALUES (?,?,?,?,?)",
                (pid, rx["doctor_name"], rx["diagnosis"], json.dumps(rx["medicines"]), rx["notes"]),
            )
            print(f"       Rx: {rx['diagnosis'][:50]}...")

        for title, content in REPORTS.get(p["name"], []):
            fname = f"{pid}_{title.replace(' ', '_').replace('/', '-')}.txt"
            (UPLOAD_DIR / fname).write_text(content, encoding="utf-8")
            conn.execute(
                "INSERT INTO reports (patient_id, doctor_name, title, file_path) VALUES (?,?,?,?)",
                (pid, next(rx["doctor_name"] for rx in PRESCRIPTIONS[p["name"]]), title, fname),
            )
            print(f"       Report: {title}")

    conn.commit()
    conn.close()
    print("\n✅ Seeding complete!")

if __name__ == "__main__":
    seed()

