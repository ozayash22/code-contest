import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Editor from "@monaco-editor/react";
import api from "../api/client";

type ProblemType = {
  id: number;
  title: string;
  difficulty: string;
  statement: string;
  constraints: string;
  input_format: string;
  output_format: string;
};

type TestCaseType = {
  id: number;
  input_data: string;
  expected_output: string;
};

export default function ProblemSolvePage() {
  const { id } = useParams();

  const [problem, setProblem] =
    useState<ProblemType | null>(null);

  const [testCases, setTestCases] = useState<TestCaseType[]>([]);

  const [code, setCode] = useState(
`n = int(input())
print(n*n)`
  );

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadProblem();
    loadVisibleCases();
  }, [id]);

  const loadProblem = async () => {
    const res = await api.get(`/api/problems/${id}`);
    setProblem(res.data);
  };

  const loadVisibleCases = async () => {
    const res = await api.get(
      `/api/test-cases/problem/${id}`
    );
    setTestCases(res.data);
  };

  const submitCode = async () => {
    setLoading(true);

    try {
      const res = await api.post("/api/submissions/", {
        problem_id: Number(id),
        language: "python",
        code,
      });

      setResult(res.data);
    } catch (err: any) {
      setResult({
        status: "ERROR",
      });
    }

    setLoading(false);
  };

  if (!problem) {
    return <div className="p-10">Loading...</div>;
  }

  return (
    <div className="h-screen grid grid-cols-2">

      {/* LEFT SIDE */}
      <div className="border-r overflow-y-auto p-6">

        <h1 className="text-2xl font-bold mb-3">
          {problem.title}
        </h1>

        <p className="mb-3 text-sm">
          Difficulty: {problem.difficulty}
        </p>

        <h2 className="font-semibold mt-4 mb-2">
          Description
        </h2>

        <p className="whitespace-pre-wrap">
          {problem.statement}
        </p>

        <h2 className="font-semibold mt-6 mb-2">
          Constraints
        </h2>

        <p className="whitespace-pre-wrap">
          {problem.constraints}
        </p>

        <h2 className="font-semibold mt-6 mb-2">
          Input Format
        </h2>

        <p>{problem.input_format}</p>

        <h2 className="font-semibold mt-6 mb-2">
          Output Format
        </h2>

        <p>{problem.output_format}</p>

        <h2 className="font-semibold mt-6 mb-3">
          Examples
        </h2>

        {testCases.map((tc, index) => (
          <div
            key={tc.id}
            className="border rounded p-3 mb-4 bg-gray-50"
          >
            <p className="font-medium mb-2">
              Example {index + 1}
            </p>

            <p className="text-sm">
              <strong>Input:</strong>
            </p>

            <pre className="bg-white p-2 border rounded mb-2">
{tc.input_data}
            </pre>

            <p className="text-sm">
              <strong>Output:</strong>
            </p>

            <pre className="bg-white p-2 border rounded">
{tc.expected_output}
            </pre>
          </div>
        ))}

      </div>

      {/* RIGHT SIDE */}
      <div className="flex flex-col">

        <div className="p-3 border-b flex justify-between">
          <h2 className="font-semibold">
            Python
          </h2>

          <button
            onClick={submitCode}
            disabled={loading}
            className="bg-black text-white px-4 py-2 rounded"
          >
            {loading ? "Submitting..." : "Submit"}
          </button>
        </div>

        <Editor
          height="70%"
          defaultLanguage="python"
          value={code}
          onChange={(value) =>
            setCode(value || "")
          }
        />

        <div className="h-[30%] border-t p-4 overflow-auto">

          <h3 className="font-semibold mb-2">
            Result
          </h3>

          {result ? (
            <div>
              <p>Status: {result.status}</p>
              <p>Runtime: {result.runtime}s</p>
              <p>
                Passed:
                {result.passed_count}/
                {result.total_tests}
              </p>
            </div>
          ) : (
            <p>No submission yet.</p>
          )}

        </div>

      </div>

    </div>
  );
}