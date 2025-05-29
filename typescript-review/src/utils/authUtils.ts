import { jwtDecode } from 'jwt-decode';
import { getSession } from 'next-auth/react';

// No type definitions for token payload
export function decodeToken(token: string) {
  try {
    return jwtDecode(token);
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
}

// No error handling for expired tokens
export function isTokenValid(token: string): boolean {
  try {
    const decoded: any = jwtDecode(token);
    return decoded.exp > Date.now() / 1000;
  } catch (error) {
    return false;
  }
}

// Security issue: roles stored directly in token without verification
export function hasRole(requiredRole: string): boolean {
  try {
    const session = getSession();
    if (!session?.accessToken) return false;
    
    const decoded: any = jwtDecode(session.accessToken);
    return decoded.roles.includes(requiredRole);
  } catch (error) {
    return false;
  }
}

// Multiple authentication checks scattered across utilities
export async function getUserPermissions(): Promise<string[]> {
  try {
    const session = await getSession();
    if (!session?.accessToken) return [];
    
    const decoded: any = jwtDecode(session.accessToken);
    return decoded.permissions || [];
  } catch (error) {
    console.error('Failed to get user permissions:', error);
    return [];
  }
}

// Hard-coded authentication check without abstraction
export function requireAuthentication(WrappedComponent: React.ComponentType<any>) {
  return function WithAuth(props: any) {
    const session = getSession();
    
    if (!session) {
      // Redirect logic duplicated across components
      if (typeof window !== 'undefined') {
        window.location.href = '/login?returnUrl=' + encodeURIComponent(window.location.pathname);
      }
      return null;
    }
    
    return <WrappedComponent {...props} />;
  };
}

// Insecure cookie handling
export function saveTokenToCookie(token: string) {
  document.cookie = `auth_token=${token}; path=/; samesite=strict;`; // Missing httpOnly and secure flags
}

