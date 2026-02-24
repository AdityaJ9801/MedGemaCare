import { useEffect, useState } from "react";
import Card from "./components/Card";
import Modal from "./components/Modal";

interface Medicine {
  name: string;
  dosage: string;
  frequency: string;
  duration: string;
}

interface Prescription {
  id: number;
  doctor_name: string;
  diagnosis: string;
  medicines: Medicine[];
  notes?: string;
  created_at: string;
}

interface Props {
  patientId: number;
  user: {
    role: "ADMIN" | "DOCTOR";
    username: string;
  };
}

export default function PrescriptionsTab({ patientId, user }: Props) {
  const [prescriptions, setPrescriptions] = useState<Prescription[]>([]);
  const [showForm, setShowForm] = useState(false);

  const [diagnosis, setDiagnosis] = useState("");
  const [notes, setNotes] = useState("");
  const [medicines, setMedicines] = useState<Medicine[]>([
    { name: "", dosage: "", frequency: "", duration: "" }
  ]);
  const [saveError, setSaveError] = useState("");
  const [saving, setSaving] = useState(false);

  const loadPrescriptions = () => {
    fetch(`/patients/${patientId}/prescriptions`)
      .then(res => res.json())
      .then(data => setPrescriptions(data));
  };

  useEffect(() => {
    loadPrescriptions();
  }, [patientId]);

  const addMedicineRow = () => {
    setMedicines([
      ...medicines,
      { name: "", dosage: "", frequency: "", duration: "" }
    ]);
  };

  const updateMedicine = (
    index: number,
    field: keyof Medicine,
    value: string
  ) => {
    const updated = [...medicines];
    updated[index][field] = value;
    setMedicines(updated);
  };

  const savePrescription = async () => {
    if (!diagnosis.trim()) {
      setSaveError("Diagnosis is required");
      return;
    }

    const validMedicines = medicines.filter(m => m.name.trim());
    if (validMedicines.length === 0) {
      setSaveError("At least one medicine is required");
      return;
    }

    setSaving(true);
    setSaveError("");

    try {
      const res = await fetch("/prescriptions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: patientId,
          doctor_name: user.username,
          diagnosis,
          medicines: validMedicines,
          notes
        })
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Save failed with status ${res.status}`);
      }

      setShowForm(false);
      setDiagnosis("");
      setNotes("");
      setMedicines([{ name: "", dosage: "", frequency: "", duration: "" }]);
      setSaveError("");
      loadPrescriptions();
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      {/* HEADER */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
        <h3 style={{ margin: 0 }}>💊 Prescriptions</h3>

        {user.role === "DOCTOR" && (
          <button className="primary-btn" onClick={() => setShowForm(true)}>
            ➕ Add Prescription
          </button>
        )}
      </div>

      {/* EMPTY STATE */}
      {prescriptions.length === 0 && (
        <Card>
          <div style={{ textAlign: "center", padding: "20px" }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>💊</div>
            <p className="muted-text">No prescriptions added yet.</p>
          </div>
        </Card>
      )}

      {/* LIST */}
      {prescriptions.map(p => (
        <Card key={p.id}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: "16px", marginBottom: "16px", paddingBottom: "16px", borderBottom: "1px solid var(--border)" }}>
            <div>
              <p style={{ margin: 0, color: "var(--text-muted)", fontSize: "13px" }}>📅 {new Date(p.created_at).toLocaleDateString()}</p>
              <p style={{ margin: "4px 0 0 0", fontWeight: "600" }}>👨‍⚕️ Dr. {p.doctor_name}</p>
            </div>
            <div style={{ textAlign: "right" }}>
              <span style={{ display: "inline-block", padding: "6px 12px", background: "var(--primary-light)", color: "var(--primary)", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>
                Rx
              </span>
            </div>
          </div>

          <div style={{ marginBottom: "16px" }}>
            <p style={{ color: "var(--text-muted)", fontSize: "12px", margin: "0 0 4px 0" }}>Diagnosis</p>
            <p style={{ margin: 0, fontWeight: "600", fontSize: "16px" }}>🔍 {p.diagnosis}</p>
          </div>

          <div style={{ marginBottom: "16px" }}>
            <p style={{ color: "var(--text-muted)", fontSize: "12px", margin: "0 0 8px 0" }}>💊 Medicines</p>
            <div style={{ display: "grid", gap: "8px" }}>
              {p.medicines.map((m, i) => (
                <div key={i} style={{ padding: "10px", background: "var(--bg)", borderRadius: "8px", borderLeft: "3px solid var(--primary)" }}>
                  <p style={{ margin: "0 0 4px 0", fontWeight: "600" }}>{m.name}</p>
                  <p style={{ margin: 0, fontSize: "13px", color: "var(--text-muted)" }}>
                    {m.dosage} • {m.frequency} • {m.duration}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {p.notes && (
            <div style={{ padding: "12px", background: "#fef3c7", borderRadius: "8px", borderLeft: "3px solid var(--warning)" }}>
              <p style={{ margin: 0, fontSize: "13px", color: "#92400e" }}>
                <b>📝 Notes:</b> {p.notes}
              </p>
            </div>
          )}
        </Card>
      ))}

      {/* MODAL FORM */}
      {showForm && (
        <Modal title="💊 Add Prescription" onClose={() => !saving && setShowForm(false)}>
          <div className="form-vertical">

            {/* ERROR MESSAGE */}
            {saveError && (
              <div className="error-message">
                ❌ {saveError}
              </div>
            )}

            {/* DOCTOR (AUTO-FILLED) */}
            <div>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "600", color: "var(--text)", marginBottom: "8px" }}>👨‍⚕️ Doctor</label>
              <input
                type="text"
                value={user.username}
                disabled
              />
            </div>

            <div>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "600", color: "var(--text)", marginBottom: "8px" }}>🔍 Diagnosis</label>
              <input
                type="text"
                placeholder="e.g., Hypertension, Diabetes"
                value={diagnosis}
                onChange={e => setDiagnosis(e.target.value)}
                disabled={saving}
              />
            </div>

            <div>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "600", color: "var(--text)", marginBottom: "8px" }}>💊 Medicines</label>

              {medicines.map((m, i) => (
                <div key={i} style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1fr", gap: "8px", marginBottom: "12px" }}>
                  <input
                    type="text"
                    placeholder="Medicine Name"
                    value={m.name}
                    onChange={e =>
                      updateMedicine(i, "name", e.target.value)
                    }
                    disabled={saving}
                  />
                  <input
                    type="text"
                    placeholder="Dosage"
                    value={m.dosage}
                    onChange={e =>
                      updateMedicine(i, "dosage", e.target.value)
                    }
                    disabled={saving}
                  />
                  <input
                    type="text"
                    placeholder="Frequency"
                    value={m.frequency}
                    onChange={e =>
                      updateMedicine(i, "frequency", e.target.value)
                    }
                    disabled={saving}
                  />
                  <input
                    type="text"
                    placeholder="Duration"
                    value={m.duration}
                    onChange={e =>
                      updateMedicine(i, "duration", e.target.value)
                    }
                    disabled={saving}
                  />
                </div>
              ))}

              <button className="btn-outline" onClick={addMedicineRow} disabled={saving}>
                ➕ Add Medicine
              </button>
            </div>

            <div>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "600", color: "var(--text)", marginBottom: "8px" }}>📝 Notes (Optional)</label>
              <textarea
                placeholder="Additional notes or instructions"
                value={notes}
                onChange={e => setNotes(e.target.value)}
                disabled={saving}
              />
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px", marginTop: "16px" }}>
              <button
                className="btn-secondary"
                onClick={() => setShowForm(false)}
                disabled={saving}
              >
                Cancel
              </button>
              <button className="primary-btn" onClick={savePrescription} disabled={saving || !diagnosis.trim()}>
                {saving ? "⏳ Saving..." : "✅ Save Prescription"}
              </button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
