import { initializeApp } from "firebase/app";
import { getFirestore, collection, getDocs } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAEjFme2sbqrIJlXciAwU0FVYR_eGRv8nQ",
  authDomain: "kinderplanet-e2b15.firebaseapp.com",
  projectId: "kinderplanet-e2b15",
  storageBucket: "kinderplanet-e2b15.firebasestorage.app",
  messagingSenderId: "768351075768",
  appId: "1:768351075768:web:b217b497886a79bb2f234d",
  measurementId: "G-9QSPF08FH8",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db, collection, getDocs };
