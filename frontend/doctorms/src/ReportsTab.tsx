import { useEffect, useState } from "react";
import Card from "./components/Card";
import Modal from "./components/Modal";

interface Report {
  id: number;
  patient_id: number;
  doctor_name: string;
  title: string;
  file_path: string;
  created_at: string;
}

interface Props {
  patientId: number;
  user: {
    role: "ADMIN" | "DOCTOR";
    username: string;
  };
}

export default function ReportsTab({ patientId, user }: Props) {
  const [reports, setReports] = useState<Report[]>([]);
  const [showForm, setShowForm] = useState(false);

  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploadError, setUploadError] = useState("");
  const [uploading, setUploading] = useState(false);

  // AI analysis state per report
  const [analyzingId, setAnalyzingId] = useState<number | null>(null);
  const [aiResults, setAiResults] = useState<Record<number, string>>({});
  const [aiErrors, setAiErrors] = useState<Record<number, string>>({});

  const loadReports = () => {
    fetch(`/patients/${patientId}/reports`)
      .then(res => res.json())
      .then(data => setReports(data));
  };

  useEffect(() => {
    loadReports();
  }, [patientId]);

  const uploadReport = async () => {
    if (!file || !title) {
      setUploadError("Please select a file and enter a title");
      return;
    }

    setUploading(true);
    setUploadError("");

    try {
      const formData = new FormData();
      formData.append("patient_id", String(patientId));
      formData.append("doctor_name", user.username);
      formData.append("title", title);
      formData.append("file", file);

      const res = await fetch("/reports", {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Upload failed with status ${res.status}`);
      }

      setShowForm(false);
      setTitle("");
      setFile(null);
      setUploadError("");
      loadReports();
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const IMAGE_EXTS = new Set(["jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "webp"]);

  const analyzeReport = async (report: Report) => {
    setAnalyzingId(report.id);
    setAiErrors(prev => { const n = { ...prev }; delete n[report.id]; return n; });
    try {
      const ext = report.file_path.split(".").pop()?.toLowerCase() ?? "";
      const isImage = IMAGE_EXTS.has(ext);

      if (isImage) {
        // ── IMAGE ANALYSIS PATH ──────────────────────────────────────────────
        // Fetch the stored image file and send it to the vision endpoint
        const fileRes = await fetch(`/files/${report.file_path}`);
        if (!fileRes.ok) throw new Error("Could not fetch image file from server");
        const blob = await fileRes.blob();

        const formData = new FormData();
        formData.append("file", blob, report.file_path);
        formData.append(
          "query",
          `Analyze this medical image titled "${report.title}" (by Dr. ${report.doctor_name}, ${new Date(report.created_at).toLocaleDateString()}). ` +
          "Provide detailed findings, clinical impression, and recommendations."
        );

        const res = await fetch("/api/v1/analyze/image", {
          method: "POST",
          body: formData,
        });
        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.detail || `Image analysis error ${res.status}`);
        }
        const data = await res.json();
        setAiResults(prev => ({ ...prev, [report.id]: data.analysis }));

      } else {
        // ── TEXT / PDF ANALYSIS PATH ─────────────────────────────────────────
        // Extract text from PDF/TXT then summarise with the text model
        let fileContent = "";
        try {
          const extractRes = await fetch(`/reports/${report.file_path}/extract-text`);
          if (extractRes.ok) {
            const extractData = await extractRes.json();
            fileContent = extractData.text || "";
          } else {
            fileContent = "[Unable to extract text from this file]";
          }
        } catch {
          fileContent = "[Error reading file]";
        }

        const prompt = `Analyze this medical report and provide a clinical summary:

Title: ${report.title}
Doctor: ${report.doctor_name}
Date: ${new Date(report.created_at).toLocaleDateString()}

Report Content:
${fileContent}

Please provide:
1. Key findings and observations
2. Clinical impression
3. Recommendations for follow-up
4. Any abnormalities or notable findings`;

        const res = await fetch("/api/v1/summarize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: prompt }),
        });
        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.detail || `API error ${res.status}`);
        }
        const data = await res.json();
        setAiResults(prev => ({ ...prev, [report.id]: data.summary }));
      }
    } catch (err: unknown) {
      setAiErrors(prev => ({ ...prev, [report.id]: err instanceof Error ? err.message : "Analysis failed" }));
    } finally {
      setAnalyzingId(null);
    }
  };

  return (
    <div>
      {/* HEADER */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
        <h3 style={{ margin: 0 }}>📄 Medical Reports</h3>

        {user.role === "DOCTOR" && (
          <button className="primary-btn" onClick={() => setShowForm(true)}>
            ⬆️ Upload Report
          </button>
        )}
      </div>

      {/* EMPTY STATE */}
      {reports.length === 0 && (
        <Card>
          <div style={{ textAlign: "center", padding: "20px" }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>📄</div>
            <p className="muted-text">No reports uploaded yet.</p>
          </div>
        </Card>
      )}

      {/* REPORT LIST */}
      {reports.map(r => (
        <Card key={r.id}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: "16px", marginBottom: "16px", paddingBottom: "16px", borderBottom: "1px solid var(--border)" }}>
            <div>
              <p style={{ margin: 0, fontSize: "18px", fontWeight: "700" }}>📄 {r.title}</p>
              <p style={{ margin: "4px 0 0 0", color: "var(--text-muted)", fontSize: "13px" }}>📅 {new Date(r.created_at).toLocaleDateString()} • 👨‍⚕️ Dr. {r.doctor_name}</p>
            </div>
            <div style={{ textAlign: "right" }}>
              <span style={{ display: "inline-block", padding: "6px 12px", background: "var(--primary-light)", color: "var(--primary)", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>
                PDF
              </span>
            </div>
          </div>

          <div style={{ display: "flex", gap: "12px", alignItems: "center", flexWrap: "wrap", marginBottom: "16px" }}>
            <a
              href={`/files/${r.file_path}`}
              target="_blank"
              rel="noopener noreferrer"
              className="primary-btn"
              style={{ textDecoration: "none" }}
            >
              📄 View / Download
            </a>

            <button
              onClick={() => analyzeReport(r)}
              disabled={analyzingId === r.id}
              className="btn-outline"
              style={{ opacity: analyzingId === r.id ? 0.6 : 1 }}
            >
              {analyzingId === r.id ? "⏳ Analyzing…" : "🧠 AI Analyze"}
            </button>
          </div>

          {aiErrors[r.id] && (
            <div className="error-message" style={{ marginBottom: "16px" }}>
              ❌ {aiErrors[r.id]}
            </div>
          )}

          {aiResults[r.id] && (
            <div className="ai-card">
              <h4>📋 AI Analysis</h4>
              <pre>{aiResults[r.id]}</pre>
            </div>
          )}
        </Card>
      ))}

      {/* UPLOAD MODAL */}
      {showForm && (
        <Modal
          title="📤 Upload Medical Report"
          onClose={() => !uploading && setShowForm(false)}
        >
          <div className="form-vertical">
            {/* ERROR MESSAGE */}
            {uploadError && (
              <div className="error-message">
                ❌ {uploadError}
              </div>
            )}

            {/* AUTO-FILLED DOCTOR */}
            <div>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "600", color: "var(--text)", marginBottom: "8px" }}>👨‍⚕️ Doctor</label>
              <input
                type="text"
                value={user.username}
                disabled
              />
            </div>

            <div>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "600", color: "var(--text)", marginBottom: "8px" }}>📄 Report Title</label>
              <input
                type="text"
                placeholder="e.g., X-Ray Report, Lab Results"
                value={title}
                onChange={e => setTitle(e.target.value)}
                disabled={uploading}
              />
            </div>

            <div>
              <label style={{ display: "block", fontSize: "14px", fontWeight: "600", color: "var(--text)", marginBottom: "8px" }}>📎 Select File</label>
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={e => setFile(e.target.files?.[0] || null)}
                disabled={uploading}
              />
              {file && (
                <p style={{ fontSize: "13px", color: "var(--text-muted)", marginTop: "8px" }}>
                  ✓ Selected: {file.name} ({(file.size / 1024).toFixed(2)} KB)
                </p>
              )}
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px", marginTop: "16px" }}>
              <button className="btn-secondary" onClick={() => setShowForm(false)} disabled={uploading}>Cancel</button>
              <button className="primary-btn" onClick={uploadReport} disabled={uploading || !file || !title}>
                {uploading ? "⏳ Uploading..." : "✅ Upload"}
              </button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}
