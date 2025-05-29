import { useState, useEffect, useCallback } from 'react';
import axios, { AxiosError, AxiosRequestConfig } from 'axios';
import { useSelector } from 'react-redux';
import { RootState } from '@/store/store';
import { apiClient } from '@/lib/api-client';
import { useUser } from '@/context/UserContext';

// Inconsistent error handling
interface DataFetchingState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

// Generic type doesn't enforce shape of API response
export function useDataFetching<T = any>(
  url: string,
  config?: AxiosRequestConfig,
  dependencies: any[] = []
): DataFetchingState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // Mixing direct Redux access with local state
  const token = useSelector((state: RootState) => state.user.token);
  const { user } = useUser();

  // Inefficient fetch implementation
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Multiple fetch mechanisms (axios direct and apiClient)
      let response;
      if (token) {
        // Direct axios call with manual token setting
        response = await axios.get(url, {
          ...config,
          headers: {
            ...config?.headers,
            Authorization: `Bearer ${token}`,
          },
        });
      } else {
        // Using apiClient which has its own token handling
        response = await apiClient.get<T>(url, config);
      }
      
      setData(response.data);
    } catch (err) {
      const axiosError = err as AxiosError;
      console.error('Error fetching data:', axiosError);
      
      // Inconsistent error handling
      if (axiosError.response?.status === 401) {
        setError('Authentication failed. Please log in again.');
      } else if (axiosError.response?.status === 403) {
        setError('You do not have permission to access this resource.');
      } else if (axiosError.response?.status === 404) {
        setError('The requested resource was not found.');
      } else {
        setError(axiosError.message || 'An unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  }, [url, config, token]);

  // Refetch triggered by too many dependencies
  useEffect(() => {
    if (!user) return;
    
    fetchData();
  }, [fetchData, user, ...dependencies]);

  // Exposed refetch lacks loading state management
  const refetch = async () => {
    await fetchData();
  };

  return { data, loading, error, refetch };
}

// Duplicate implementation for POST requests
export function useDataSubmission<T = any, D = any>(
  url: string,
  config?: AxiosRequestConfig
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const submit = async (submitData: D) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.post<T>(url, submitData, config);
      setData(response);
      return response;
    } catch (err) {
      const axiosError = err as AxiosError;
      const errorMessage = axiosError.response?.data?.message || axiosError.message || 'An unknown error occurred';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, submit };
}

export default useDataFetching;

