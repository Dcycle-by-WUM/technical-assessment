// Dashboard page - Combining all components with issues
'use client';

import React, { useState, useEffect } from 'react';
import UserProfile from '@/components/UserProfile';
import DataList from '@/components/DataList';
import { useData } from '@/hooks/useData';
import * as api from '@/utils/api';

// No proper type for the component
export default function Dashboard() {
  // Inefficient: Multiple unnecessary state variables
  const [selectedItem, setSelectedItem] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [lastRefresh, setLastRefresh] = useState(new Date());
  
  // Inefficient: Using the custom hook with issues
  const { data: users, loading: usersLoading, error: usersError, refresh: refreshUsers } = useData('users');
  const { data: items, loading: itemsLoading, error: itemsError } = useData('items');
  
  // Anti-pattern: Multiple useEffects that could be combined
  useEffect(() => {
    // Side effect in useEffect without cleanup
    const timer = setInterval(() => {
      console.log('Checking for updates...');
      refreshUsers();
      setLastRefresh(new Date());
    }, 60000);
    
    // Missing return cleanup function
  }, []);
  
  useEffect(() => {
    // Security issue: Directly using localStorage in components
    const userRole = localStorage.getItem('user_role');
    setIsAdmin(userRole === 'admin');
    
    // This could create memory leaks or unexpected behaviors
    document.title = `Dashboard - ${userRole} View`;
  }, []);
  
  // Anti-pattern: Function recreated on every render
  const handleProfileUpdate = (data) => {
    // Security issue: Directly passing user input to API
    api.updateUserSettings(data)
      .then((response) => {
        // Anti-pattern: Directly manipulating DOM outside React
        document.getElementById('update-message').innerHTML = 'Profile updated!';
        refreshUsers();
      })
      .catch((error) => {
        console.error('Failed to update profile:', error);
      });
  };
  
  // Performance issue: Complex calculations in render
  const totalActiveItems = items ? 
    items.filter(item => item.status === 'active').length : 0;
  
  // Accessibility issue: No proper loading states or error handling UI
  return (
    <div className="dashboard-container">
      <h1>User Dashboard</h1>
      
      {/* Missing proper loading state */}
      {usersLoading && <p>Loading...</p>}
      
      {/* Security issue: Potentially exposing error details */}
      {usersError && <p>Error: {usersError.toString()}</p>}
      
      {/* Accessibility issue: Improper heading hierarchy */}
      <h3>User Profile</h3>
      
      {/* Type issues: Passing untyped props */}
      {users && users.length > 0 && (
        <UserProfile 
          name={users[0].name}
          email={users[0].email}
          role={users[0].role}
          stats={users[0].stats}
          joinDate={new Date(users[0].created_at).toLocaleDateString()}
          onUpdate={handleProfileUpdate}
        />
      )}
      
      {/* Performance issue: Unnecessary re-renders */}
      <div style={{ marginTop: '2rem' }}>
        <h3>Items ({totalActiveItems} active)</h3>
        <button onClick={() => {
          // Inefficient: Creating a new date object on every click
          setLastRefresh(new Date());
          refreshUsers();
        }}>
          Refresh Data
        </button>
        <p>Last refreshed: {lastRefresh.toLocaleTimeString()}</p>
        <div id="update-message"></div>
        
        {/* Performance issue: Passing non-memoized callback */}
        <DataList 
          items={items} 
          onItemSelect={(item) => {
            console.log('Selected item:', item);
            setSelectedItem(item);
          }}
        />
      </div>
      
      {/* Accessibility issue: Non-semantic HTML */}
      <div style={{ 
        position: 'fixed', 
        bottom: 0, 
        left: 0, 
        right: 0, 
        background: '#f0f0f0',
        padding: '1rem',
        textAlign: 'center'
      }}>
        {/* Security issue: Potential XSS vulnerability */}
        <div dangerouslySetInnerHTML={{ 
          __html: `<p>Logged in as ${users?.[0]?.name || 'User'}</p>` 
        }} />
        
        {/* Accessibility issue: Non-descriptive button text */}
        <button onClick={() => {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user_role');
          window.location.href = '/login';
        }}>
          X
        </button>
      </div>
    </div>
  );
}

