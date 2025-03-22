// Save array of objects to localStorage
export const saveToLocalStorage = (key, data) => {
    if (typeof window !== "undefined") {
      window.localStorage.setItem(key, JSON.stringify(data));
    }
  };
  
  // Fetch array of objects from localStorage
  export const fetchFromLocalStorage = (key) => {
    if (typeof window !== "undefined") {
      const data = window.localStorage.getItem(key);
      return data ? JSON.parse(data) : [];
    }
    return [];
  };
  