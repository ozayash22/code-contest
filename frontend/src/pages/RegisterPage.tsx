import { useState } from "react";
import api from "../api/client";
import { useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const nav = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: ""
  });

  const register = async () => {
    await api.post("/api/auth/register", form);

    alert("Registered");

    nav("/login");
  };

  return (
    <div className="p-10 max-w-md mx-auto">
      <h1 className="text-2xl mb-4">
        Register
      </h1>

      <input
        className="border p-2 w-full mb-2"
        placeholder="Name"
        onChange={(e) =>
          setForm({
            ...form,
            name: e.target.value
          })
        }
      />

      <input
        className="border p-2 w-full mb-2"
        placeholder="Email"
        onChange={(e) =>
          setForm({
            ...form,
            email: e.target.value
          })
        }
      />

      <input
        type="password"
        className="border p-2 w-full mb-4"
        placeholder="Password"
        onChange={(e) =>
          setForm({
            ...form,
            password: e.target.value
          })
        }
      />

      <button
        onClick={register}
        className="bg-black text-white px-4 py-2"
      >
        Register
      </button>
    </div>
  );
}