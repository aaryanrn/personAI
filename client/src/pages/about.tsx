import Logo from "@/components/Logo";
import Head from "next/head";
import Link from "next/link";

export default function About() {
  const currentYear = new Date().getFullYear();

  const developers = [
    { name: "Aaryan Agrawal", email: "itsaaryanagrawal@gmail.com" },
    { name: "Anmol Bhusal", email: "anmol52490@gmail.com" },
    { name: "Bhishan Pangeni", email: "bhishanpangeni2003@gmail.com" },
    { name: "Raj Kumar Sah", email: "rajsah5556@gmail.com" },
  ];

  return (
    <>
      <Head>
        <title>personAI - About Us</title>
        <meta name="description" content="Learn more about personAI and the developers behind it." />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      <div className="bg-base text-gray-900 min-h-screen flex flex-col font-sans">
        {/* Header */}
        <header className="container mx-auto py-6 px-4 flex justify-between items-center">
            <Link href="/">
                <Logo/>
            </Link>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex flex-col items-center px-6 py-12">
          <h1 className="text-2xl font-bold mb-8">
            <span className="text-black">About</span> <span className="text-prim">Us</span>
          </h1>
          
          {/* About personAI */}
          <p className="text-lg text-gray-700 text-center max-w-3xl">
            <b>personAI</b> is an advanced AI-driven voice assistant designed to offer <b>personalized conversations</b> by adapting to various personas. Unlike traditional AI assistants, personAI allows users to <b>select or create personas</b> that align with their preferences, making interactions more engaging and meaningful.
          </p>

          <div className="mt-12 max-w-4xl text-center space-y-8">
            {/* Our Mission */}
            <div>
              <h2 className="text-2xl font-bold mb-4">
                <span className="text-black">Our</span> <span className="text-prim">Mission</span>
              </h2>
              <p className="text-lg text-gray-700">
                Our mission is to <b>redefine human-AI interaction</b> by creating a digital assistant that understands and adapts to individual users. We believe AI should be more than just a tool—it should be a <b>companion</b> that enhances productivity, learning, and entertainment.
              </p>
            </div>

            {/* Our Vision */}
            <div>
              <h2 className="text-2xl font-bold mb-4">
                <span className="text-black">Our</span> <span className="text-prim">Vision</span>
              </h2>
              <p className="text-lg text-gray-700">
                We envision a world where AI assistants are <b>more human-like, dynamic, and customizable</b>. personAI strives to bridge the gap between artificial intelligence and human conversation, enabling a future where <b>AI adapts to individuals</b>, rather than the other way around.
              </p>
            </div>
          </div>

          {/* Developer Section */}
          <h2 className="text-2xl font-bold mt-16 mb-6">
            <span className="text-black">Meet The</span> <span className="text-prim">Developers</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {developers.map((dev) => (
              <div key={dev.name} className="border-2 border-prim p-6 rounded-lg shadow-lg text-center w-60">
              <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto flex items-center justify-center text-2xl font-bold text-prim">
                {dev.name.charAt(0)}
              </div>
              <p className="mt-4 text-lg font-bold text-black">{dev.name}</p>
              <p className="text-gray-700 text-lg">BMS College of Engineering</p>
              {/* Email Section with Proper Wrapping */}
              <p className="text-prim mt-2 text-lg break-words w-full px-2">
                {dev.email}
              </p>
            </div>
            
            ))}
          </div>
        </main>

        {/* Footer */}
        <footer className="py-4 bg-gray-900 text-white text-center w-full">
          <p className="text-lg">© {currentYear} personAI. All rights reserved.</p>
        </footer>
      </div>
    </>
  );
}