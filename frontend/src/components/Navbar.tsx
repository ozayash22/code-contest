import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <div className="border-b px-6 py-4 flex justify-between">
      <Link to="/" className="font-bold text-xl">
        CodeContest
      </Link>

      <div className="space-x-4">
        <Link to="/contests">Contests</Link>

        {user?.role === "ADMIN" && (
          <Link to="/admin">Admin</Link>
        )}

        {!user ? (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        ) : (
          <button onClick={logout}>
            Logout
          </button>
        )}
      </div>
    </div>
  );
}