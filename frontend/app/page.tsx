"use client";

import { useState, useEffect, useRef } from "react";
import axios from "axios";

type Role = {
  role: string;
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  improvement_steps: string[];
};

type EvaluationResponse = {
  roles: Role[];
  best_fit: string;
  summary: string;
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [github, setGithub] = useState("");
  const [linkedin, setLinkedin] = useState("");
  const [result, setResult] = useState<EvaluationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);

  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const timeouts = useRef<NodeJS.Timeout[]>([]);

  const BACKEND_URL = "https://fitstack-lot0.onrender.com";

  // Warm backend on first load
  useEffect(() => {
    fetch(`${BACKEND_URL}/`).catch(() => {});
  }, []);

  // Clear timeouts on unmount
  useEffect(() => {
    return () => {
      timeouts.current.forEach(clearTimeout);
    };
  }, []);

  const handleSubmit = async () => {
    if (!file) {
      fileInputRef.current?.click();
      return;
    }

    setLoading(true);
    setResult(null);
    setStep(1);

    // Structured step progression
    timeouts.current = [
      setTimeout(() => setStep(2), 1000),
      setTimeout(() => setStep(3), 2500),
      setTimeout(() => setStep(4), 4500),
    ];

    const formData = new FormData();
    formData.append("resume_file", file);
    formData.append("github_link", github);
    formData.append("linkedin_link", linkedin);

    const start = Date.now();

    try {
      const res = await axios.post(
        `${BACKEND_URL}/evaluate`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      const elapsed = Date.now() - start;
      if (elapsed < 3000) {
        await new Promise((r) => setTimeout(r, 3000 - elapsed));
      }

      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Something went wrong. Please try again.");
    }

    setLoading(false);
    setStep(0);
  };

  const getScoreColor = (score: number) => {
    if (score >= 75) return "bg-emerald-500";
    if (score >= 50) return "bg-amber-500";
    return "bg-rose-500";
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="max-w-6xl mx-auto px-8 py-12">

        {/* Header */}
        <div className="mb-10">
          <h1 className="text-4xl font-semibold tracking-tight">
            Role Clarity Report
          </h1>
          <p className="text-gray-500 mt-2">
            AI-powered evaluation of your technical profile alignment.
          </p>
        </div>

        {/* Upload Section */}
        {!loading && (
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm mb-10">
            <div className="grid md:grid-cols-3 gap-4">

              <input
                type="file"
                accept=".pdf"
                ref={fileInputRef}
                onChange={(e) => {
                  if (e.target.files && e.target.files.length > 0) {
                    setFile(e.target.files[0]);
                  }
                }}
                className="border border-gray-200 p-2 rounded-lg"
              />

              <input
                type="text"
                placeholder="GitHub link (optional)"
                value={github}
                onChange={(e) => setGithub(e.target.value)}
                className="border border-gray-200 p-2 rounded-lg"
              />

              <input
                type="text"
                placeholder="LinkedIn link (optional)"
                value={linkedin}
                onChange={(e) => setLinkedin(e.target.value)}
                className="border border-gray-200 p-2 rounded-lg"
              />
            </div>

            <button
              onClick={handleSubmit}
              className="mt-6 bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition"
            >
              Generate Report
            </button>
          </div>
        )}

        {/* Loading Section */}
        {loading && (
          <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm mb-8">
            <h3 className="text-lg font-semibold">Generating Report</h3>

            <ul className="mt-6 space-y-3 text-sm">
              <li className={step >= 1 ? "text-gray-900" : "text-gray-400"}>
                {step > 1 ? "✔ " : ""} Parsing Resume
              </li>
              <li className={step >= 2 ? "text-gray-900" : "text-gray-400"}>
                {step > 2 ? "✔ " : ""} Extracting Skills
              </li>
              <li className={step >= 3 ? "text-gray-900" : "text-gray-400"}>
                {step > 3 ? "✔ " : ""} Evaluating Role Alignment
              </li>
              <li className={step >= 4 ? "text-gray-900" : "text-gray-400"}>
                Building Scorecards
              </li>
            </ul>

            <div className="grid md:grid-cols-2 gap-6 mt-8">
              {[1,2,3,4].map((i) => (
                <div key={i} className="animate-pulse bg-gray-200 h-32 rounded-2xl" />
              ))}
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <>
            <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm mb-8">
              <p className="text-sm text-gray-500">Best Fit Role</p>
              <h2 className="text-2xl font-semibold mt-1">
                {result.best_fit}
              </h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {result.roles.map((role) => (
                <div
                  key={role.role}
                  className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200"
                >
                  <h3 className="text-lg font-semibold">{role.role}</h3>

                  <div className="mt-4">
                    <div className="flex justify-between text-sm text-gray-500">
                      <span>Alignment Score</span>
                      <span>{role.score}/100</span>
                    </div>
                    <div className="w-full bg-gray-200 h-2 rounded-full mt-2">
                      <div
                        className={`${getScoreColor(role.score)} h-2 rounded-full`}
                        style={{ width: `${role.score}%` }}
                      />
                    </div>
                  </div>

                  <div className="mt-6">
                    <p className="text-sm font-medium text-gray-700 mb-3">
                      Strengths
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {role.matched_skills.map((skill) => (
                        <span
                          key={skill}
                          className="px-3 py-1 bg-emerald-50 text-emerald-700 text-sm rounded-md border border-emerald-200"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mt-6">
                    <p className="text-sm font-medium text-gray-700 mb-3">
                      Skill Gaps
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {role.missing_skills.map((skill) => (
                        <span
                          key={skill}
                          className="px-3 py-1 bg-rose-50 text-rose-700 text-sm rounded-md border border-rose-200"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

      </div>
    </div>
  );
}