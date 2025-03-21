import { getFirestore, doc, setDoc } from "firebase/firestore";
import { getApp, initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID
};

let app;
try {
  app = getApp();
} catch (error) {
  app = initializeApp(firebaseConfig);
}

const db = getFirestore(app);

const sendDataToFirebase = async (persona, identity) => {
  try {
    const formData = { ...persona, identity };
    await setDoc(doc(db, "personas", identity), formData);
    console.log("Data successfully written to Firebase");
  } catch (error) {
    console.error("Error writing document: ", error);
  }
};

export default sendDataToFirebase;
