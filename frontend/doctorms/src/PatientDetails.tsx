import { useState } from "react";
import PrescriptionsTab from "./PrescriptionsTab";
import ReportsTab from "./ReportsTab";

interface Patient {
  id: number;
  name: string;
  age: number;
  gender: string;
}

interface User {
  role: "ADMIN" | "DOCTOR";
  username: string;
}

interface Props {
  patient: Patient;
  user: User;
}

type Tab = "OVERVIEW" | "PRESCRIPTIONS" | "REPORTS" | "AI";

interface Medicine { name: string; dosage: string; frequency: string; duration: string; }
interface Prescription { doctor_name: string; diagnosis: string; medicines: Medicine[]; notes?: string; created_at: string; }
interface Report { title: string; doctor_name: string; created_at: string; }

export default function PatientDetails({ patient, user }: Props) {
  const [activeTab, setActiveTab] = useState<Tab>("OVERVIEW");

  // AI Summary state
  const [loadingAI, setLoadingAI] = useState(false);
  const [aiSummary, setAiSummary] = useState<string | null>(null);
  const [aiError, setAiError] = useState<string | null>(null);
  const [customQ, setCustomQ] = useState("");

  const generateSummary = async () => {
    setLoadingAI(true);
    setAiSummary(null);
    setAiError(null);

    try {
      // 1. Fetch patient data in parallel
      const [rxRes, rpRes] = await Promise.all([
        fetch(`/patients/${patient.id}/prescriptions`),
        fetch(`/patients/${patient.id}/reports`),
      ]);
      const prescriptions: Prescription[] = await rxRes.json();
      const reports: Report[] = await rpRes.json();

      // 2. Build EHR text
      let ehr = `Patient: ${patient.name}, ${patient.age} years old (${patient.gender})\n\n`;

      if (prescriptions.length > 0) {
        ehr += "=== PRESCRIPTIONS ===\n";
        prescriptions.forEach((p, i) => {
          ehr += `${i + 1}. Date: ${new Date(p.created_at).toLocaleDateString()}\n`;
          ehr += `   Doctor: ${p.doctor_name}\n`;
          ehr += `   Diagnosis: ${p.diagnosis}\n`;
          ehr += `   Medicines: ${p.medicines.map(m => `${m.name} ${m.dosage}, ${m.frequency}, ${m.duration}`).join("; ")}\n`;
          if (p.notes) ehr += `   Notes: ${p.notes}\n`;
        });
        ehr += "\n";
      }

      if (reports.length > 0) {
        ehr += "=== MEDICAL REPORTS ===\n";
        reports.forEach((r, i) => {
          ehr += `${i + 1}. Title: ${r.title} | Doctor: ${r.doctor_name} | Date: ${new Date(r.created_at).toLocaleDateString()}\n`;
        });
      }

      // 3. Call real AI API
      const query = customQ.trim() ||
        "Provide a comprehensive clinical summary including diagnoses, current medications, and recommended follow-up actions.";

      const res = await fetch("/api/v1/analyze/ehr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ehr_text: ehr, query }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `API error ${res.status}`);
      }

      const data = await res.json();
      setAiSummary(data.analysis);
    } catch (err: unknown) {
      setAiError(err instanceof Error ? err.message : "Failed to generate summary");
    } finally {
      setLoadingAI(false);
    }
  };

  return (
    <div className="card" style={{ marginTop: "30px" }}>
      <h2>👤 Patient Profile</h2>

      {/* TABS */}
      <div className="tabs">
        <TabButton label="📋 Overview" active={activeTab === "OVERVIEW"} onClick={() => setActiveTab("OVERVIEW")} />
        <TabButton label="💊 Prescriptions" active={activeTab === "PRESCRIPTIONS"} onClick={() => setActiveTab("PRESCRIPTIONS")} />
        <TabButton label="📄 Reports" active={activeTab === "REPORTS"} onClick={() => setActiveTab("REPORTS")} />
        <TabButton label="🧠 AI Summary" active={activeTab === "AI"} onClick={() => setActiveTab("AI")} />
      </div>

      {/* TAB CONTENT */}
      {activeTab === "OVERVIEW" && (
        <div className="tab-content">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "20px" }}>
            <div style={{ padding: "16px", background: "var(--bg)", borderRadius: "12px", border: "1px solid var(--border)" }}>
              <p style={{ color: "var(--text-muted)", fontSize: "12px", margin: "0 0 4px 0" }}>Full Name</p>
              <p style={{ fontSize: "18px", fontWeight: "700", margin: 0 }}>👤 {patient.name}</p>
            </div>
            <div style={{ padding: "16px", background: "var(--bg)", borderRadius: "12px", border: "1px solid var(--border)" }}>
              <p style={{ color: "var(--text-muted)", fontSize: "12px", margin: "0 0 4px 0" }}>Age</p>
              <p style={{ fontSize: "18px", fontWeight: "700", margin: 0 }}>🎂 {patient.age} years</p>
            </div>
            <div style={{ padding: "16px", background: "var(--bg)", borderRadius: "12px", border: "1px solid var(--border)" }}>
              <p style={{ color: "var(--text-muted)", fontSize: "12px", margin: "0 0 4px 0" }}>Gender</p>
              <p style={{ fontSize: "18px", fontWeight: "700", margin: 0 }}>⚪ {patient.gender}</p>
            </div>
          </div>

          {user.role !== "ADMIN" && (
            <p className="muted-text" style={{ marginTop: "20px" }}>ℹ️ Only admin can edit patient details</p>
          )}
        </div>
      )}

      {activeTab === "PRESCRIPTIONS" && (
        <PrescriptionsTab patientId={patient.id} user={user} />
      )}

      {activeTab === "REPORTS" && (
        <ReportsTab patientId={patient.id} user={user} />
      )}

      {/* 🧠 AI SUMMARY TAB */}
      {activeTab === "AI" && (
        <div className="tab-content">
          <p className="muted-text" style={{ marginBottom: "16px" }}>
            ℹ️ The AI will analyze this patient's prescriptions and reports to generate a clinical summary.
            You can also ask a specific question below.
          </p>

          <textarea
            placeholder="Optional: ask a specific question (e.g. 'Are there any drug interactions?')"
            value={customQ}
            onChange={e => setCustomQ(e.target.value)}
            style={{ marginBottom: "16px" }}
          />

          <button
            className="primary-btn"
            onClick={generateSummary}
            disabled={loadingAI}
          >
            {loadingAI ? "⏳ Analyzing patient data…" : "🧠 Generate AI Summary"}
          </button>

          {aiError && (
            <div className="error-message" style={{ marginTop: "16px" }}>
              ❌ {aiError}
            </div>
          )}

          {aiSummary && (
            <div className="ai-card">
              <h4>🩺 AI Clinical Summary</h4>
              <pre>{aiSummary}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* TAB BUTTON */
function TabButton({
  label,
  active,
  onClick
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      className={`tab-btn ${active ? "tab-active" : ""}`}
      onClick={onClick}
      type="button"
    >
      {label}
    </button>
  );
}
