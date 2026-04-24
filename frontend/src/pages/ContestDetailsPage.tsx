import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/client";

export default function ContestDetailsPage() {
  const { id } = useParams();
  const [problems, setProblems] = useState([]);

  useEffect(() => {
    api.get(`/api/problems/contest/${id}`)
      .then((res) => setProblems(res.data));
  }, [id]);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-6">
        Contest Problems
      </h1>

      {problems.map((p: any) => (
        <Link
          key={p.id}
          to={`/problem/${p.id}`}
          className="block border p-4 mb-3 rounded"
        >
          <h2>{p.title}</h2>
          <p>{p.difficulty}</p>
        </Link>
      ))}
    </div>
  );
}