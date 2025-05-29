import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';
import dashboardReducer from './dashboardSlice';
import analyticsReducer from './analyticsSlice';
import notificationsReducer from './notificationsSlice';
import settingsReducer from './settingsSlice';
import integrationsReducer from './integrationsSlice';
import teamsReducer from './teamsSlice';
import billingReducer from './billingSlice';
import reportsReducer from './reportsSlice';
import eventsReducer from './eventsSlice';

// Too many slices in a single store
const store = configureStore({
  reducer: {
    user: userReducer,
    dashboard: dashboardReducer,
    analytics: analyticsReducer,
    notifications: notificationsReducer,
    settings: settingsReducer,
    integrations: integrationsReducer,
    teams: teamsReducer,
    billing: billingReducer,
    reports: reportsReducer,
    events: eventsReducer,
  },
  // No middleware configuration
  // No performance optimizations
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;

