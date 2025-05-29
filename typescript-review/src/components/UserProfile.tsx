// UserProfile.tsx - Component with prop type issues
import React, { useState } from 'react';
import Image from 'next/image';

// Missing proper type definitions and using 'any'
const UserProfile = (props: any) => {
  // Incorrectly typed state - should be more specific
  const [userData, setUserData] = useState({} as any);
  
  // No type for event parameter
  const handleChange = (event) => {
    const { name, value } = event.target;
    setUserData({ ...userData, [name]: value });
  };

  // Function with inconsistent return types
  function formatUserRole(role) {
    if (role === 'admin') {
      return { label: 'Administrator', level: 3 };
    } else if (role === 'user') {
      return 'Standard User';
    } else {
      return null;
    }
  }

  return (
    <div className="user-profile-container">
      <h2>User Profile</h2>
      
      {/* Missing alt text for accessibility */}
      <img 
        src={props.avatarUrl || '/default-avatar.png'} 
        className="avatar"
        width={100}
        height={100}
      />
      
      <div className="user-details">
        {/* Unsafe usage of dangerouslySetInnerHTML */}
        <h3 dangerouslySetInnerHTML={{ __html: props.name || 'User' }}></h3>
        
        <p>Email: {props.email || 'No email provided'}</p>
        
        {/* Type inconsistency - may not be a string */}
        <p>Role: {formatUserRole(props.role)}</p>
        
        <div className="user-stats">
          {/* Direct DOM manipulation without React */}
          <div ref={(el) => {
            if (el) {
              el.innerHTML = `<strong>Posts:</strong> ${props.stats?.posts || 0}`;
            }
          }}></div>
          <p><strong>Joined:</strong> {props.joinDate || 'Unknown'}</p>
        </div>
      </div>
      
      {/* Form without proper accessibility attributes */}
      <form>
        <input
          name="name"
          placeholder="Update name"
          onChange={handleChange}
          value={userData.name || ''}
        />
        <button onClick={(e) => {
          e.preventDefault();
          // Type safety issue - props.onUpdate might not be a function
          props.onUpdate(userData);
        }}>
          Update Profile
        </button>
      </form>
    </div>
  );
};

export default UserProfile;

