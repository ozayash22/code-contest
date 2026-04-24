import { useEffect, useState } from "react";
import api from "../api/client";
import { Link } from "react-router-dom";

export default function ContestPage() {
  const [contests, setContests] = useState([]);

  useEffect(() => {
    api.get("/api/contests").then((res) => setContests(res.data));
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-6">Contests</h1>

      {contests.map((c: any) => (
        <Link
          to={`/contest/${c.id}`}
          key={c.id}
          className="block border p-4 mb-3 rounded"
        >
          <h2>{c.title}</h2>
          <p>{c.description}</p>
          <p>{c.status}</p>
        </Link>
      ))}
    </div>
  );
}
