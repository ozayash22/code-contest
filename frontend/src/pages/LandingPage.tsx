import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="p-20 text-center">
      <h1 className="text-5xl font-bold mb-6">
        CodeContest
      </h1>

      <p className="mb-8">
        Real-time coding contests platform
      </p>

      <Link
        to="/login"
        className="bg-black text-white px-5 py-3 mr-4"
      >
        Login
      </Link>

      <Link
        to="/register"
        className="border px-5 py-3"
      >
        Register
      </Link>
    </div>
  );
}