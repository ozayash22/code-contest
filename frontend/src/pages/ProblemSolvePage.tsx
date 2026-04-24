import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Editor from "@monaco-editor/react";
import api from "../api/client";

export default function ProblemSolvePage() {
  const { id } = useParams();

  const [problem, setProblem] = useState<any>(null);
  const [code, setCode] = useState(
`n = int(input())
print(n*n)`
  );

  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    api.get(`/api/problems/${id}`)
      .then((res) => setProblem(res.data));
  }, [id]);

  const submit = async () => {
    const res = await api.post("/api/submissions/", {
      problem_id: Number(id),
      language: "python",
      code
    });

    setResult(res.data);
  };

  if (!problem) return <div>Loading...</div>;

  return (
    <div className="grid grid-cols-2 h-screen">

      <div className="p-6 overflow-auto">
        <h1 className="text-2xl font-bold mb-4">
          {problem.title}
        </h1>

        <p className="mb-4">{problem.statement}</p>

        <p>Difficulty: {problem.difficulty}</p>
      </div>

      <div className="p-6 flex flex-col">

        <Editor
          height="70vh"
          defaultLanguage="python"
          value={code}
          onChange={(v) => setCode(v || "")}
        />

        <button
          onClick={submit}
          className="bg-black text-white px-4 py-2 mt-4"
        >
          Submit
        </button>

        {result && (
          <div className="mt-4 border p-4 rounded">
            <p>Status: {result.status}</p>
            <p>Runtime: {result.runtime}s</p>
            <p>
              Passed:
              {result.passed_count}/
              {result.total_tests}
            </p>
          </div>
        )}

      </div>
    </div>
  );
}