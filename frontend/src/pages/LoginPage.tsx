import { useState } from "react";
import api from "../api/client";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    const res = await api.post("/api/auth/login", {
      email,
      password
    });

    localStorage.setItem(
      "token",
      res.data.access_token
    );

    alert("Logged in");
  };

  return (
    <div className="p-10 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">
        Login
      </h1>

      <input
        className="border p-2 w-full mb-3"
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        className="border p-2 w-full mb-3"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button
        onClick={login}
        className="bg-black text-white px-4 py-2"
      >
        Login
      </button>
    </div>
  );
}