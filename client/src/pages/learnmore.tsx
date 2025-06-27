import Logo from "@/components/Logo";
import Head from "next/head";
import Link from "next/link";

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
  },
  {
    icon: (
      <svg className="w-8 h-8 text-prim" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 20v-6m0 0V4m0 10l-3-3m3 3l3-3" /></svg>
    ),
    title: "Seamless Sync",
    desc: "Access your AI and chats from any device, anytime."
  },
  {
    icon: (
      <svg className="w-8 h-8 text-prim" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 19v-6m0 0V5m0 8l-3-3m3 3l3-3" /><circle cx="12" cy="12" r="10" /></svg>
    ),
    title: "Instant Answers",
    desc: "Get quick, accurate responses to your questions in real time."
  },
  {
    icon: (
      <svg className="w-8 h-8 text-prim" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path d="M15 9a3 3 0 0 1-6 0" /><path d="M9 13h6" /></svg>
    ),
    title: "Emotion Recognition",
    desc: "Your AI can sense your mood and adapt its responses for a more human-like experience."
  }
];

const useCases = [
  {
    title: "Education",
    desc: "AI tutors adapt to students' learning styles for personalized education.",
    icon: "🎓"
  },
  {
    title: "Customer Support",
    desc: "AI assistants provide personalized solutions and 24/7 support.",
    icon: "🤖"
  },
  {
    title: "Healthcare",
    desc: "Virtual AI companions support mental well-being and health tracking.",
    icon: "💡"
  },
  {
    title: "AI Friend",
    desc: "Enjoy companionship, conversation, and emotional support from your AI friend.",
    icon: "💖"
  },
  {
    title: "Entertainment",
    desc: "Enjoy games, quizzes, and creative storytelling with your AI.",
    icon: "🎮"
  },
  {
    title: "Accessibility",
    desc: "Voice and text interfaces make AI accessible to everyone.",
    icon: "♿"
  }
];

export default function LearnMore() {
  return (
    <>
      <Head>
        <title>Learn More - personAI</title>
        <meta name="description" content="Discover more about personAI and how it enhances AI interactions." />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>
      <div className="bg-base dark:bg-black min-h-screen flex flex-col font-sans text-gray-900 dark:text-gray-100">
        {/* Header */}
        <header className="container mx-auto py-6 px-6 flex justify-between items-center">
          <Link href="/">
            <Logo />
          </Link>
        </header>
        {/* Hero Section */}
        <section className="flex flex-col items-center justify-center py-10 px-4">
          <svg width="120" height="120" viewBox="0 0 180 180" fill="none" xmlns="http://www.w3.org/2000/svg" className="animate-bounce-slow mb-4">
            <circle cx="90" cy="90" r="80" fill="#18181b" stroke="#fff" strokeWidth="4" />
            <ellipse cx="60" cy="90" rx="12" ry="18" fill="#fff" />
            <ellipse cx="120" cy="90" rx="12" ry="18" fill="#fff" />
            <circle cx="60" cy="90" r="6" fill="#6f37f0" />
            <circle cx="120" cy="90" r="6" fill="#6f37f0" />
            <rect x="70" y="120" width="40" height="10" rx="5" fill="#fff" />
            <rect x="80" y="30" width="20" height="20" rx="10" fill="#6f37f0" />
          </svg>
          <h1 className="text-5xl md:text-6xl font-extrabold text-center mb-4">Discover <span className="text-prim">personAI</span></h1>
          <p className="text-xl text-center max-w-2xl text-gray-600 dark:text-gray-300 mb-6">
            Next-generation AI voice assistant with <span className="text-prim font-semibold">custom personas</span>, real-time voice, and privacy-first design. Experience the future of human-AI interaction.
          </p>
          <Link href="/signup">
            <button className="px-8 py-3 bg-prim text-white text-lg rounded-lg shadow-lg transition transform hover:scale-105 hover:bg-purple-700 font-bold">
              Get Started
            </button>
          </Link>
        </section>
        {/* Features Grid */}
        <section className="container mx-auto px-4 py-10">
          <h2 className="text-3xl font-bold text-center mb-10">Key Features</h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {features.map(f => (
              <div key={f.title} className="flex flex-col items-center bg-white dark:bg-gray-900 rounded-xl shadow-md px-6 py-8 border border-gray-200 dark:border-gray-700">
                {f.icon}
                <div className="font-bold mt-4 text-center text-black">{f.title}</div>
                <div className="text-sm text-gray-500 dark:text-gray-300 text-center mt-2">{f.desc}</div>
              </div>
            ))}
          </div>
        </section>
        {/* Use Cases */}
        <section className="container mx-auto px-4 py-10">
          <h2 className="text-3xl font-bold text-center mb-10">Real-World Applications</h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {useCases.map(u => (
              <div key={u.title} className="flex flex-col items-center bg-gray-50 dark:bg-gray-800 rounded-xl shadow px-6 py-8 border border-gray-200 dark:border-gray-700">
                <div className="text-4xl mb-2">{u.icon}</div>
                <div className="font-bold text-lg text-black dark:text-white mb-1">{u.title}</div>
                <div className="text-sm text-gray-600 dark:text-gray-300 text-center">{u.desc}</div>
              </div>
            ))}
          </div>
        </section>
        {/* Testimonial */}
        <section className="container mx-auto px-4 py-10">
          <div className="max-w-2xl mx-auto bg-white dark:bg-gray-900 rounded-xl shadow-lg px-8 py-8 text-center">
            <div className="text-2xl text-prim mb-2">“</div>
            <div className="italic text-lg text-gray-700 dark:text-gray-200">
              personAI made my daily tasks so much easier. The custom persona feels like a real companion!
            </div>
            <div className="mt-4 text-xs text-gray-500 dark:text-gray-400">— Early Adopter</div>
          </div>
        </section>
        {/* Back to Home Button */}
        <div className="flex justify-center mb-10">
          <Link href="/">
            <button className="px-8 py-3 bg-prim text-white text-lg rounded-lg shadow-lg transition transform hover:scale-105 hover:bg-purple-700 font-bold">
              Back to Home
            </button>
          </Link>
        </div>
        {/* Footer */}
        <footer className="py-6 bg-gray-900 text-white text-center">
          <p className="text-lg">© {new Date().getFullYear()} personAI. All rights reserved.</p>
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
    </>
  );
}