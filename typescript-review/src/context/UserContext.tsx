import React, { createContext, useContext, useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { setUser } from '@/store/userSlice';

// Type definitions are incomplete
type UserRole = 'admin' | 'user' | 'manager';

interface UserData {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  teamId?: string;
  preferences?: Record<string, any>; // Any type used
}

interface UserContextType {
  user: UserData | null;
  loading: boolean;
  error: string | null;
  updateUserPreferences: (preferences: Record<string, any>) => Promise<void>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { data: session } = useSession();
  const [user, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const dispatch = useDispatch();

  // Multiple data sources for user data - session, API, and Redux
  useEffect(() => {
    const fetchUserData = async () => {
      if (session?.user?.email) {
        try {
          setLoading(true);
          // Direct API call in component without abstraction
          const response = await axios.get(`/api/users/profile?email=${session.user.email}`);
          setUserData(response.data);
          dispatch(setUser(response.data));
        } catch (err) {
          console.error('Failed to fetch user data', err);
          setError('Failed to load user data');
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [session, dispatch]);

  // No caching or optimistic updates
  const updateUserPreferences = async (preferences: Record<string, any>) => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    try {
      const response = await axios.patch(`/api/users/${user.id}/preferences`, { preferences });
      setUserData((prevUser) => {
        if (!prevUser) return null;
        return {
          ...prevUser,
          preferences: {
            ...prevUser.preferences,
            ...preferences,
          },
        };
      });
      return response.data;
    } catch (err) {
      console.error('Failed to update user preferences', err);
      throw err;
    }
  };

  return (
    <UserContext.Provider value={{ user, loading, error, updateUserPreferences }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

