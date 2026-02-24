
import { useEffect, useMemo, useRef, useState } from "react";
import PatientDetails from "./PatientDetails";
import Login from "./Login";
import "./App.css";

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

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(false);   // false until user logs in
  const [loadError, setLoadError] = useState("");
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);

  // 🔍 Search & Filters (Doctor)
  const [search, setSearch] = useState("");
  const [genderFilter, setGenderFilter] = useState("ALL");
  const [minAge, setMinAge] = useState("");
  const [maxAge, setMaxAge] = useState("");

  // Debounced search — only updates 300 ms after the user stops typing
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const handleSearchChange = (value: string) => {
    setSearch(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => setDebouncedSearch(value), 300);
  };

  // Memoised filter — only recomputes when the debounced inputs actually change
  const filteredPatients = useMemo(() => patients.filter(p => {
    const matchesSearch =
      p.name.toLowerCase().includes(debouncedSearch.toLowerCase()) ||
      String(p.id).includes(debouncedSearch);
    const matchesGender = genderFilter === "ALL" || p.gender === genderFilter;
    const matchesMinAge = minAge === "" || p.age >= Number(minAge);
    const matchesMaxAge = maxAge === "" || p.age <= Number(maxAge);
    return matchesSearch && matchesGender && matchesMinAge && matchesMaxAge;
  }), [patients, debouncedSearch, genderFilter, minAge, maxAge]);

  // Admin-only form state
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("Male");
  const [addError, setAddError] = useState("");
  const [adding, setAdding] = useState(false);

  const loadPatients = () => {
    setLoading(true);
    setLoadError("");
    fetch("/patients")
      .then(res => {
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        return res.json();
      })
      .then(data => {
        setPatients(data);
        setLoading(false);
      })
      .catch(err => {
        setLoadError(err.message || "Failed to load patients. Is the server running?");
        setLoading(false);
      });
  };

  useEffect(() => {
    if (user) loadPatients();
  }, [user]);

  const logout = () => {
    setUser(null);
    setSelectedPatient(null);
  };

  const addPatient = async () => {
    if (!name.trim() || !age) {
      setAddError("Name and age are required");
      return;
    }

    const ageNum = Number(age);
    if (ageNum < 0 || ageNum > 150) {
      setAddError("Age must be between 0 and 150");
      return;
    }

    setAdding(true);
    setAddError("");

    try {
      const res = await fetch("/patients", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          age: ageNum,
          gender
        })
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Add failed with status ${res.status}`);
      }

      setName("");
      setAge("");
      setGender("Male");
      setAddError("");
      loadPatients();
    } catch (err) {
      setAddError(err instanceof Error ? err.message : "Add patient failed");
    } finally {
      setAdding(false);
    }
  };

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <div className="app-container">
      {/* HEADER */}
      <div className="app-header">
        <div>
          <h1>🏥 Doctor PMS</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "14px", margin: "4px 0 0 0" }}>Patient Management System</p>
        </div>

        <div className="user-box">
          <div style={{ textAlign: "right" }}>
            <div className="username">👤 {user.username}</div>
            <span className="role">{user.role}</span>
          </div>
          <button className="logout-btn" onClick={logout}>
            🚪 Logout
          </button>
        </div>
      </div>

      {/* ADMIN ONLY: ADD PATIENT */}
      {user.role === "ADMIN" && (
        <div className="card">
          <h3>➕ Add New Patient</h3>

          {addError && (
            <div className="error-message" style={{ marginBottom: "16px" }}>
              ❌ {addError}
            </div>
          )}

          <div className="form-grid">
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={e => setName(e.target.value)}
              disabled={adding}
            />

            <input
              type="number"
              placeholder="Age"
              value={age}
              onChange={e => setAge(e.target.value)}
              disabled={adding}
            />

            <select
              value={gender}
              onChange={e => setGender(e.target.value)}
              disabled={adding}
            >
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>

            <button className="primary-btn" onClick={addPatient} disabled={adding || !name.trim() || !age}>
              {adding ? "⏳ Adding..." : "✅ Add Patient"}
            </button>
          </div>
        </div>
      )}

      {user.role === "DOCTOR" && (
        <p className="muted-text">
          Only admin can add new patients
        </p>
      )}

      {/* DOCTOR SEARCH & FILTERS */}
      {user.role === "DOCTOR" && (
        <div className="filter-bar">
          <input
            type="text"
            placeholder="🔍 Search by name or ID"
            value={search}
            onChange={e => handleSearchChange(e.target.value)}
          />

          <select
            value={genderFilter}
            onChange={e => setGenderFilter(e.target.value)}
          >
            <option value="ALL">👥 All Genders</option>
            <option value="Male">👨 Male</option>
            <option value="Female">👩 Female</option>
            <option value="Other">⚪ Other</option>
          </select>

          <input
            type="number"
            placeholder="Min Age"
            value={minAge}
            onChange={e => setMinAge(e.target.value)}
          />

          <input
            type="number"
            placeholder="Max Age"
            value={maxAge}
            onChange={e => setMaxAge(e.target.value)}
          />
        </div>
      )}

      {/* PATIENT LIST */}
      <div className="table-card">
        {loading && (
          <div style={{ padding: "40px", textAlign: "center" }}>
            <div style={{ fontSize: "32px", marginBottom: "12px" }}>⏳</div>
            <p style={{ color: "var(--text-muted)" }}>Loading patients…</p>
          </div>
        )}

        {!loading && loadError && (
          <div className="error-message" style={{ margin: "16px" }}>
            ⚠️ {loadError}
          </div>
        )}

        {!loading && !loadError && filteredPatients.length === 0 && (
          <div style={{ padding: "40px", textAlign: "center" }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>😴</div>
            <p className="muted-text">No patients found.</p>
          </div>
        )}

        {!loading && !loadError && filteredPatients.length > 0 && (
          <table className="patient-table">
            <thead>
              <tr>
                <th>#</th>
                <th>👤 Name</th>
                <th>🎂 Age</th>
                <th>⚪ Gender</th>
              </tr>
            </thead>

            <tbody>
              {filteredPatients.map(p => (
                <tr
                  key={p.id}
                  className={
                    selectedPatient?.id === p.id ? "row-active" : ""
                  }
                  onClick={() => setSelectedPatient(p)}
                >
                  <td>{p.id}</td>
                  <td className="bold">{p.name}</td>
                  <td>{p.age}</td>
                  <td>{p.gender}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>


      {/* PATIENT DETAILS */}
      {selectedPatient && (
        <PatientDetails patient={selectedPatient} user={user} />
      )}
    </div>
  );

}

export default App;