import React, { useState } from "react";
import Link from "next/link";
import ThemeToggle from "@/components/button/ThemeToggle";
import { useRouter } from "next/router";

const features = [
  {
    icon: (
      <svg className="w-8 h-8 text-prim" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" /><path d="M19 10v2a7 7 0 0 1-14 0v-2" /><line x1="12" x2="12" y1="19" y2="22" /></svg>
    ),
    title: "Custom Personas",
    desc: "Create and use unique AI personalities tailored to you."
  },
  {
    icon: (
      <svg className="w-8 h-8 text-prim" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" /></svg>
    ),
    title: "Voice AI",
    desc: "Talk to your AI using natural voice recognition."
  },
  {
    icon: (
      <svg className="w-8 h-8 text-prim" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" /><path d="M7 11V7a5 5 0 0 1 10 0v4" /></svg>
    ),
    title: "Privacy First",
    desc: "Your data is secure and private, always."
  }
];

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || "Login failed");
        setLoading(false);
        return;
      }
      // Success
      localStorage.setItem("personai_logged_in", "true");
      router.push("/");
    } catch (err) {
      setError("Network error");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-base dark:bg-black text-gray-900 dark:text-white font-sans relative overflow-hidden">
      <div className="absolute top-6 right-8 z-20">
        <ThemeToggle />
      </div>
      <div className="flex flex-1 flex-col md:flex-row items-center justify-center w-full max-w-6xl mx-auto py-12 gap-12">
        {/* Left: Welcome, Features, Mascot */}
        <div className="flex-1 flex flex-col items-center md:items-start gap-8">
          {/* Mascot */}
          <div className="mb-2">
            <svg width="120" height="120" viewBox="0 0 180 180" fill="none" xmlns="http://www.w3.org/2000/svg" className="animate-bounce-slow">
              <circle cx="90" cy="90" r="80" fill="#18181b" stroke="#fff" strokeWidth="4" />
              <ellipse cx="60" cy="90" rx="12" ry="18" fill="#fff" />
              <ellipse cx="120" cy="90" rx="12" ry="18" fill="#fff" />
              <circle cx="60" cy="90" r="6" fill="#6f37f0" />
              <circle cx="120" cy="90" r="6" fill="#6f37f0" />
              <rect x="70" y="120" width="40" height="10" rx="5" fill="#fff" />
              <rect x="80" y="30" width="20" height="20" rx="10" fill="#6f37f0" />
            </svg>
          </div>
          {/* Welcome */}
          <h1 className="text-4xl md:text-5xl font-extrabold text-center md:text-left mb-2">Welcome to <span className="text-prim">personAI</span></h1>
          <p className="text-lg text-center md:text-left max-w-md text-gray-600 dark:text-gray-300">Your personalized AI assistant with a unique persona. Sign up or log in to get started!</p>
          {/* Features */}
          <div className="flex gap-4 mt-4">
            {features.map(f => (
              <div key={f.title} className="flex flex-col items-center bg-white dark:bg-gray-900 rounded-xl shadow-md px-4 py-3 w-36 border border-gray-200 dark:border-gray-700">
                {f.icon}
                <div className="font-bold mt-2 text-center text-black">{f.title}</div>
                <div className="text-xs text-gray-500 dark:text-gray-300 text-center">{f.desc}</div>
              </div>
            ))}
          </div>
          {/* Testimonial / Fun Fact */}
          <div className="mt-6 bg-gray-100 dark:bg-gray-800 rounded-lg px-6 py-4 shadow text-center md:text-left max-w-md">
            <span className="italic text-gray-700 dark:text-gray-200">“I love how I can create my own AI persona. It feels like talking to a real friend!”</span>
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">— Beta User</div>
          </div>
          {/* Learn More Link */}
          <div className="mt-4">
            <Link href="/learnmore" className="text-prim font-semibold hover:underline">Learn more about personAI →</Link>
          </div>
        </div>
        {/* Right: Login Form */}
        <form onSubmit={handleSubmit} className="flex-1 z-10 bg-white dark:bg-gray-900/90 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-2xl p-10 w-full max-w-md flex flex-col gap-6 backdrop-blur-md">
          <h2 className="text-3xl font-extrabold text-center text-prim tracking-tight mb-2">Login</h2>
          <p className="text-center text-gray-500 dark:text-gray-300 mb-4">Login to your personAI account</p>
          <label className="block">
            <span className="block mb-1 font-medium text-black">Email</span>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-black focus:outline-none focus:ring-2 focus:ring-prim" placeholder="you@email.com" required />
          </label>
          <label className="block">
            <span className="block mb-1 font-medium text-black">Password</span>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-black focus:outline-none focus:ring-2 focus:ring-prim" placeholder="••••••••" required />
          </label>
          {error && <div className="text-red-500 text-center font-semibold">{error}</div>}
          <button type="submit" className="w-full py-3 rounded-lg bg-prim text-white font-bold text-lg shadow-lg hover:bg-purple-700 transition" disabled={loading}>{loading ? "Logging in..." : "Login"}</button>
          <div className="text-center text-gray-500 dark:text-gray-300 mt-2">
            Don&apos;t have an account? <Link href="/signup" className="text-prim font-semibold hover:underline">Sign up</Link>
          </div>
        </form>
      </div>
      {/* Footer */}
      <footer className="w-full py-4 text-center text-xs text-gray-400 mt-8">
        © {new Date().getFullYear()} personAI. Made with <span className="text-prim">♥</span> by Momo lovers.
      </footer>
      <style jsx>{`
        .animate-bounce-slow {
          animation: bounce 3s infinite;
        }
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
      `}</style>
    </div>
  );
} 