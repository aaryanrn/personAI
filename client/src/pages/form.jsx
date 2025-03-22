import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import Link from "next/link";
import { prebuiltPersonas } from "../personas/preBuiltPersonas";
import { fetchFromLocalStorage, saveToLocalStorage } from "../utils/localStorage";


export default function PersonaSelection() {
  const [showForm, setShowForm] = useState(false);
  const [selectedPersona, setSelectedPersona] = useState(null);
  const [persona, setPersona] = useState({
    // type:"",
    persona_name: "",
    sex: "",
    traits: "",
    tone: "",
    purpose: "",
    response_type: "",
    backstory: "",
    avatar:"agent.jpeg",
  });

  
  const router = useRouter();
  const currentYear = new Date().getFullYear();
  
  
  // const personas=prebuiltPersonas;
  const [personas,setPersonas]=useState(prebuiltPersonas);

  // Fetch persona data from localStorage on component mount
  useEffect(() => {
    const savedPersonas = fetchFromLocalStorage("persona");

    setPersonas((prevPersonas) => {
      const newPersonas = savedPersonas.filter(savedPersona => 
        !prevPersonas.some(existingPersona => existingPersona.persona_name === savedPersona.persona_name)
      );
      
      return [...prevPersonas, ...newPersonas];
    });

    console.log(personas);
    
    // setPersonas(savedPersonas);
  }, []);

  // useEffect(() => {
  //   console.log(personas);
  // }, [personas]); // This will log every time personas state changes
  

  const handleAddPersona = (e) => {
    e.preventDefault();
    console.log("Custom Persona Created:", persona);
    setShowForm(false);
    const newPersona = persona;
    const updatedPersonas = [...personas, newPersona];
    
    // Update state with the new persona and save to localStorage
    setPersonas(updatedPersonas);
    saveToLocalStorage("persona", updatedPersonas);
  };
  // const handleSubmit = (e) => {
  //   // console.log("submit custom",persona)
  //   e.preventDefault();
  //   console.log("Custom Persona Created:", persona);
  //   router.push({
  //     pathname: '/home',
  //     query: { persona: JSON.stringify(persona) },
  //   });
  // };

  const handlePrebuiltSelection = (persona_name) => {
    const selected = personas.find((p) => p.persona_name === persona_name);
    console.log(selected)
    // console.log("thype",persona_name)
    while (!selected) {
      console.log("in loop not selected any persona",selected)
    }
    // console.log("out loop ",selected)
    setPersona(selected);
    // setSelectedPersona(persona_name);
    setShowForm(false);
    // setErrors({});
    router.push({
      pathname: '/home',
      query: { persona: JSON.stringify(selected) },
    });
    // setSelectedPersona(persona_name);
    // setShowForm(false);
  };

  const handleCustomSelection = () => {
    setSelectedPersona("custom");
    setShowForm(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPersona((prev) => ({ ...prev, [name]: value }));
  };



  return (
    <>
      <Head>
        <title>personAI - Select Your Persona</title>
        <meta name="description" content="Choose or create a personalized AI persona." />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>

      <div className="bg-base text-gray-900 min-h-screen flex flex-col font-sans">
        {/* Header */}
        <header className="container mx-auto py-6 px-4 flex justify-between items-center">
          <Link href="/">
            <div className="flex items-center gap-2 -ml-6">
              {/* Logo */}
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-prim">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" x2="12" y1="19" y2="22"></line>
              </svg>
              <span className="text-3xl font-bold text-black">personAI</span>
            </div>
          </Link>
        </header>

        <main className="flex-1 flex flex-col items-center overflow-y-auto pb-24 px-6">
          {!showForm ? (
            <>
              <h1 className="text-4xl font-bold mb-8">
                <span className="text-black">Choose Your</span> <span className="text-prim">Persona</span>
              </h1>

              {/* Persona Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-12">
                {personas.map((p) => {
                  // console.log("p ",p)
                  const words = p.persona_name.split(" ");
                  const firstPart = words.slice(0, -1).join(" ");
                  const lastWord = words[words.length - 1];

                  return (
                    <button
                      key={p.persona_name}
                      onClick={() => handlePrebuiltSelection(p.persona_name)}
                      className="persona-card border-2 border-prim bg-white w-72 h-96 p-6 rounded-lg flex flex-col items-center transition hover:scale-105"
                    >
                      <div className="w-full h-72 rounded-lg bg-gray-200 flex items-center justify-center">
                        <img src={p.avatar} alt={p.persona_name} className="w-5/6 h-5/6 object-cover rounded-lg" />
                      </div>
                      <p className="mt-4 text-xl font-bold">
                        <span className="text-black">{firstPart}</span> <span className="text-prim">{lastWord}</span>
                      </p>
                    </button>
                  );
                })}

                {/* Custom Persona Card */}
                <button
                  onClick={handleCustomSelection}
                  className="persona-card border-2 border-prim bg-white w-72 h-96 p-6 rounded-lg flex flex-col items-center transition hover:scale-105"
                >
                  <div className="w-full h-72 rounded-lg bg-gray-200 flex items-center justify-center">
                    <span className="text-7xl font-bold text-prim">+</span>
                  </div>
                  <p className="mt-4 text-xl font-bold">
                    <span className="text-black">Custom</span> <span className="text-prim">Persona</span>
                  </p>
                </button>
              </div>

            </>
          ) : (
            /* Custom Persona Form */
            <form onSubmit={handleAddPersona} className="w-full max-w-lg bg-white p-8 rounded-lg shadow-lg border-2 border-prim">
              <h1 className="text-4xl font-bold mb-8">
                <span className="text-black">Create</span> <span className="text-prim">Persona</span>
              </h1>
              <div className="space-y-5">
                {[
                  { name: "persona_name", placeholder: "e.g., Friendly AI" },
                  { name: "sex", placeholder: "e.g., Male/Female/Other" },
                  { name: "traits", placeholder: "e.g., Helpful, Witty" },
                  { name: "tone", placeholder: "e.g., Professional, Casual" },
                  { name: "purpose", placeholder: "e.g., AI tutor, Assistant" },
                  { name: "response_type", placeholder: "e.g., Short, Detailed" },
                  { name: "backstory", placeholder: "e.g., AI created in 2030 to help users" },
                ].map(({ name, placeholder }) => (
                  <div key={name}>
                    <label className="block text-gray-700 font-medium">{name.replace("_", " ").toUpperCase()}</label>
                    {name === "backstory" ? (
                      <textarea
                        name={name}
                        value={persona[name]}
                        onChange={handleInputChange}
                        placeholder={placeholder}
                        className="w-full px-4 py-2 h-40 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-prim"
                      />
                    ) : (
                      <input
                        type="text"
                        name={name}
                        value={persona[name]}
                        onChange={handleInputChange}
                        placeholder={placeholder}
                        required
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-prim"
                      />
                    )}
                  </div>
                ))}
              </div>

              <div className="flex justify-between mt-6">
                <button type="button" onClick={() => setShowForm(false)} className="px-6 py-3 border border-gray-500 text-gray-700 rounded-md font-medium hover:bg-gray-100 transition">
                  Back
                </button>
                <button type="submit" className="px-6 py-3 bg-prim text-white rounded-md font-medium hover:bg-purple-700 transition">
                  Save Persona
                </button>
              </div>
            </form>
          )}
        </main>

        {/* Footer */}
        <footer className="py-4 bg-gray-900 text-white text-center w-full">
          <p className="text-sm">© {currentYear} personAI. All rights reserved.</p>
        </footer>
      </div>
    </>
  );
}