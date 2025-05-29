// useData.ts - Custom hook with state management issues
import { useState, useEffect } from 'react';

// Missing proper return type
export function useData(endpoint) {
  // Overly broad types
  const [data, setData] = useState<any>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<any>(null);
  
  // State used for tracking refresh operations, but initialized inside a useEffect
  const [refreshCounter, setRefreshCounter] = useState(0);
  
  // Missing dependency array causing infinite loop potential
  useEffect(() => {
    let isMounted = true;
    
    const fetchData = async () => {
      setLoading(true);
      try {
        // No error handling for malformed JSON
        const response = await fetch(`/api/${endpoint}`);
        const result = await response.json();
        
        // Race condition: Not checking if component is still mounted
        setData(result);
        setError(null);
      } catch (err) {
        // Poor error handling
        console.error('Error fetching data:', err);
        setError('An error occurred. Please try again later.');
        setData([]);
      } finally {
        // State updates after possible unmount
        setLoading(false);
      }
    };
    
    fetchData();
    
    // Missing cleanup function
  }, [endpoint, refreshCounter]);  // Missing dependency: refreshCounter
  
  // Function that creates state update functions without memoization
  const refresh = () => {
    // Direct state mutation instead of using setter
    setRefreshCounter(refreshCounter + 1);
  };
  
  // Excessive state updates
  const updateItem = (id, newData) => {
    // Inefficient state update that re-renders everything
    const newItems = [...data];
    const index = newItems.findIndex(item => item.id === id);
    
    if (index !== -1) {
      newItems[index] = { ...newItems[index], ...newData };
      setData(newItems);
    }
  };
  
  // Creating a new object on every render
  return {
    data, 
    loading, 
    error,
    refresh,
    updateItem
  };
}

