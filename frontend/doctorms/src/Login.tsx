import { useState } from "react";

interface Props {
  onLogin: (user: { role: "ADMIN" | "DOCTOR"; username: string }) => void;
}

export default function Login({ onLogin }: Props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = () => {
    setError("");
    setLoading(true);

    fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    })
      .then(res => {
        if (!res.ok) throw new Error("Invalid credentials");
        return res.json();
      })
      .then(data => onLogin(data))
      .catch(() => setError("Invalid username or password"))
      .finally(() => setLoading(false));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") handleLogin();
  };

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      padding: "20px"
    }}>
      <div style={{
        width: "100%",
        maxWidth: "420px",
        padding: "40px",
        background: "white",
        borderRadius: "16px",
        boxShadow: "0 20px 60px rgba(0, 0, 0, 0.3)",
        animation: "slideUp 0.5s ease"
      }}>
        {/* HEADER */}
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
          <div style={{
            fontSize: "48px",
            marginBottom: "12px"
          }}>🏥</div>
          <h1 style={{
            fontSize: "28px",
            fontWeight: "700",
            color: "#1e293b",
            margin: "0 0 8px 0"
          }}>Doctor PMS</h1>
          <p style={{
            color: "#64748b",
            fontSize: "14px",
            margin: 0
          }}>Patient Management System</p>
        </div>

        {/* ERROR MESSAGE */}
        {error && (
          <div style={{
            padding: "12px 16px",
            background: "#fee2e2",
            border: "1px solid #fecaca",
            borderRadius: "8px",
            color: "#991b1b",
            fontSize: "14px",
            marginBottom: "20px",
            textAlign: "center"
          }}>
            ⚠️ {error}
          </div>
        )}

        {/* FORM */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <div>
            <label style={{
              display: "block",
              fontSize: "14px",
              fontWeight: "600",
              color: "#1e293b",
              marginBottom: "8px"
            }}>Username</label>
            <input
              type="text"
              placeholder="admin or doctor"
              value={username}
              onChange={e => setUsername(e.target.value)}
              onKeyPress={handleKeyPress}
              style={{
                width: "100%",
                padding: "12px",
                border: "1px solid #e2e8f0",
                borderRadius: "8px",
                fontSize: "14px",
                transition: "all 0.2s ease",
                boxSizing: "border-box"
              }}
            />
          </div>

          <div>
            <label style={{
              display: "block",
              fontSize: "14px",
              fontWeight: "600",
              color: "#1e293b",
              marginBottom: "8px"
            }}>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              style={{
                width: "100%",
                padding: "12px",
                border: "1px solid #e2e8f0",
                borderRadius: "8px",
                fontSize: "14px",
                transition: "all 0.2s ease",
                boxSizing: "border-box"
              }}
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={loading || !username || !password}
            style={{
              width: "100%",
              padding: "12px",
              background: loading ? "#cbd5e1" : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontSize: "16px",
              fontWeight: "600",
              cursor: loading ? "not-allowed" : "pointer",
              transition: "all 0.2s ease",
              transform: loading ? "scale(1)" : "scale(1)",
              marginTop: "8px"
            }}
            onMouseEnter={(e) => {
              if (!loading) (e.target as HTMLButtonElement).style.transform = "translateY(-2px)";
            }}
            onMouseLeave={(e) => {
              (e.target as HTMLButtonElement).style.transform = "translateY(0)";
            }}
          >
            {loading ? "🔄 Logging in..." : "Login"}
          </button>
        </div>

        {/* DEMO CREDENTIALS */}
        <div style={{
          marginTop: "24px",
          padding: "16px",
          background: "#f0f4ff",
          borderRadius: "8px",
          fontSize: "13px",
          color: "#1e293b"
        }}>
          <p style={{ margin: "0 0 8px 0", fontWeight: "600" }}>📝 Demo Credentials:</p>
          <p style={{ margin: "4px 0" }}>👤 <strong>admin</strong> / admin123</p>
          <p style={{ margin: "4px 0" }}>👨‍⚕️ <strong>doctor</strong> / doctor123</p>
        </div>
      </div>

      <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}
