import Logo from "@/components/Logo";
import Head from "next/head";
import Link from "next/link";

export default function LearnMore() {
  return (
    <>
      <Head>
        <title>Learn More - personAI</title>
        <meta name="description" content="Discover more about personAI and how it enhances AI interactions." />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      <div className="min-h-screen flex flex-col font-sans">
        {/* Header */}
        <header className="container mx-auto py-6 px-6 flex justify-between items-center">
            <Link href="/">
                <Logo />
            </Link>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex flex-col items-center px-6 py-12">
          <h1 className="text-6xl font-extrabold text-center mb-12 text-gray-900">
            Learn <span className="text-prim">More</span>
          </h1>

          <div className="max-w-4xl text-center text-lg text-gray-700 space-y-12 bg-white shadow-lg p-10 rounded-xl">
            <p className="leading-relaxed">
              <span className="font-bold">personAI</span> is a next-generation AI-powered voice assistant that offers
              <span className="text-prim"> personalized AI personas</span> for natural, dynamic conversations.
              Unlike traditional assistants, personAI adapts to individual communication styles, allowing users to
              select or create AI personalities for engaging interactions.
            </p>

            {/* Features */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">How personAI Works</h2>
              <ul className="space-y-4 text-left">
                <li className="flex items-start gap-3">
                  <span className="text-prim text-2xl">◆</span>
                  <span><span className="font-bold">Voice Processing:</span> Uses <span className="text-prim">LiveKit WebRTC</span> for real-time interactions.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-prim text-2xl">◆</span>
                  <span><span className="font-bold">AI Persona Selection:</span> Choose from prebuilt or custom AI personalities.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-prim text-2xl">◆</span>
                  <span><span className="font-bold">Natural Language Processing:</span> Understands and responds like a human using advanced LLMs.</span>
                </li>
              </ul>
            </div>

            {/* Use Cases */}
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Real-World Applications</h2>
              <ul className="space-y-4 text-left">
                <li className="flex items-start gap-3">
                  <span className="text-prim text-2xl">◆</span>
                  <span><span className="font-bold">Education:</span> AI tutors adapt to students&apos; learning styles.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-prim text-2xl">◆</span>
                  <span><span className="font-bold">Customer Support:</span> AI assistants provide personalized solutions.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-prim text-2xl">◆</span>
                  <span><span className="font-bold">Healthcare:</span> Virtual AI companions support mental well-being.</span>
                </li>
              </ul>
            </div>
          </div>

          {/* CTA Button */}
          <Link href="/">
            <button className="mt-10 px-8 py-3 bg-prim text-white text-lg rounded-lg shadow-lg transition transform hover:scale-105 hover:bg-purple-700">
              Back to Home
            </button>
          </Link>
        </main>

        {/* Footer */}
        <footer className="py-6 bg-gray-900 text-white text-center">
          <p className="text-lg">© {new Date().getFullYear()} personAI. All rights reserved.</p>
        </footer>
      </div>
    </>
  );
}