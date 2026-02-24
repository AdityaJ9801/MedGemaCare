export default function Card({ children }: { children: React.ReactNode }) {
  return (
    <div style={{
      background: "var(--card)",
      border: "1px solid var(--border)",
      borderRadius: "10px",
      padding: "16px",
      marginBottom: "16px",
      boxShadow: "0 4px 10px rgba(0,0,0,0.05)"
    }}>
      {children}
    </div>
  );
}
