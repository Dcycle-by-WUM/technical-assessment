import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';
import { Provider as ReduxProvider } from 'react-redux';
import { ApolloProvider } from '@apollo/client';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ThemeProvider } from '@/context/ThemeContext';
import store from '@/store/store';
import { apolloClient } from '@/lib/apollo-client';
import Layout from '@/components/layout/Layout';
import { ToastProvider } from '@/context/ToastContext';
import { FeatureFlagProvider } from '@/context/FeatureFlagContext';
import { UserProvider } from '@/context/UserContext';
import UserActivityTracker from '@/components/common/UserActivityTracker';
import ErrorBoundary from '@/components/common/ErrorBoundary';

// Initialize QueryClient without proper config
const queryClient = new QueryClient();

// Global unhandled promise rejection listener
if (typeof window !== 'undefined') {
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    // No centralized error tracking
  });
}

export default function App({ Component, pageProps: { session, ...pageProps } }: AppProps) {
  return (
    <ErrorBoundary>
      <SessionProvider session={session}>
        <ReduxProvider store={store}>
          <ApolloProvider client={apolloClient}>
            <QueryClientProvider client={queryClient}>
              <ThemeProvider>
                <ToastProvider>
                  <FeatureFlagProvider>
                    <UserProvider>
                      <UserActivityTracker />
                      <Layout>
                        <Component {...pageProps} />
                      </Layout>
                    </UserProvider>
                  </FeatureFlagProvider>
                </ToastProvider>
              </ThemeProvider>
            </QueryClientProvider>
          </ApolloProvider>
        </ReduxProvider>
      </SessionProvider>
    </ErrorBoundary>
  );
}

