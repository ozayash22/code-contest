import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const nav = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    const res = await api.post(
      "/api/auth/login",
      {
        email,
        password,
      }
    );

    login(
      res.data.access_token,
      res.data.role
    );

    if (res.data.role === "ADMIN") {
      nav("/admin");
    } else {
      nav("/contests");
    }
  };

  return (
    <div className="p-10 max-w-md mx-auto">
      <h1 className="text-2xl mb-4">
        Login
      </h1>

      <input
        className="border p-2 w-full mb-2"
        placeholder="Email"
        onChange={(e) =>
          setEmail(e.target.value)
        }
      />

      <input
        type="password"
        className="border p-2 w-full mb-4"
        placeholder="Password"
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <button
        onClick={submit}
        className="bg-black text-white px-4 py-2"
      >
        Login
      </button>
    </div>
  );
}