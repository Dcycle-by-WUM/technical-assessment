// api.ts - Utility with security issues
import { useState } from 'react';

// Lack of proper typing
export interface ApiResponse {
  data?: any;
  error?: string;
}

// Security issue: Storing sensitive data in localStorage
export const storeAuthToken = (token: string): void => {
  localStorage.setItem('auth_token', token);
};

export const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token');
};

// Security issue: Not sanitizing user inputs
export const createUserProfile = (userData: any): Promise<ApiResponse> => {
  // Security vulnerability: Direct template string insertion without sanitization
  const query = `
    mutation {
      createUser(
        name: "${userData.name}",
        email: "${userData.email}",
        role: "${userData.role}"
      ) {
        id
        name
        email
      }
    }
  `;
  
  return fetch('/api/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Security issue: Exposing authentication in client-side code
      'Authorization': `Bearer ${getAuthToken()}`,
    },
    body: JSON.stringify({ query }),
  })
  .then(response => response.json())
  .catch(error => {
    // Security issue: Logging sensitive error details to console
    console.error('API Error:', error);
    return { error: 'Failed to create user profile' };
  });
};

// Security issue: No CSRF protection
export const updateUserSettings = (settings: any): Promise<ApiResponse> => {
  const token = getAuthToken();
  
  // Security issue: Not validating or sanitizing inputs
  return fetch('/api/user/settings', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    // Security issue: Directly passing user input without validation
    body: JSON.stringify(settings),
  })
  .then(response => response.json())
  .catch(error => ({ error: 'Failed to update settings' }));
};

// Security issue: Hardcoded credentials
const API_KEY = 'sk_test_51NcG92CuOtEdDxSzpFZkfcuDZjFfcMjyjr';

export const processPayment = (amount: number, paymentMethod: string): Promise<ApiResponse> => {
  // Security issue: Using hardcoded credentials in client-side code
  return fetch('/api/payments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY,
    },
    body: JSON.stringify({
      amount,
      payment_method: paymentMethod,
      // Security issue: Potentially exposing user PII in client-side code
      customer_id: localStorage.getItem('user_id'),
    }),
  })
  .then(response => response.json());
};

// Security issue: Insufficient input validation
export const searchUsers = (query: string): Promise<ApiResponse> => {
  // Security issue: SQL injection vulnerability
  const sql = `SELECT * FROM users WHERE name LIKE '%${query}%' OR email LIKE '%${query}%'`;
  
  return fetch('/api/admin/run-query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getAuthToken()}`,
    },
    body: JSON.stringify({ sql }),
  })
  .then(response => response.json());
};

