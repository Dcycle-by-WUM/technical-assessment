import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useQuery } from 'react-query';
import { useUser } from '@/context/UserContext';
import DashboardLayout from '@/components/dashboard/DashboardLayout';
import MetricsPanel from '@/components/dashboard/MetricsPanel';
import ActivityFeed from '@/components/dashboard/ActivityFeed';
import RecentProjects from '@/components/dashboard/RecentProjects';
import TeamMembers from '@/components/dashboard/TeamMembers';
import NotificationsPanel from '@/components/dashboard/NotificationsPanel';
import { fetchDashboardData } from '@/api/dashboard';
import { updateDashboard } from '@/store/dashboardSlice';
import Loading from '@/components/common/Loading';
import ErrorDisplay from '@/components/common/ErrorDisplay';
import type { RootState } from '@/store/store';
import { socket } from '@/lib/socket';
import usePermissions from '@/hooks/usePermissions';

// No proper typings for API responses
interface DashboardDataResponse {
  metrics: any[];
  activities: any[];
  projects: any[];
  team: any[];
  notifications: any[];
}

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const { user, loading: userLoading } = useUser();
  const dashboardState = useSelector((state: RootState) => state.dashboard);
  const [realTimeUpdates, setRealTimeUpdates] = useState<any[]>([]);
  const { hasPermission } = usePermissions();

  // Multiple data fetching mechanisms - Redux, React Query, and direct useState
  const { data, isLoading, error } = useQuery<DashboardDataResponse>(
    ['dashboardData', user?.id],
    () => fetchDashboardData(user?.id || ''),
    {
      enabled: !!user?.id,
      // No retry configuration
      // No cache time settings
    }
  );

  // Direct socket integration in component
  useEffect(() => {
    if (!user?.id) return;

    socket.connect();
    socket.on('dashboard-update', (update) => {
      setRealTimeUpdates((prev) => [...prev, update]);
    });

    return () => {
      socket.off('dashboard-update');
      socket.disconnect();
    };
  }, [user?.id]);

  // Duplicate data management
  useEffect(() => {
    if (data) {
      dispatch(updateDashboard(data));
    }
  }, [data, dispatch]);

  // Multiple loading states
  if (userLoading || isLoading) {
    return <Loading />;
  }

  // Multiple error handling approaches
  if (error) {
    return <ErrorDisplay error={error} />;
  }

  if (!user) {
    return <ErrorDisplay error="Authentication required" />;
  }

  return (
    <DashboardLayout>
      <div className="dashboard-container">
        <h1>Welcome, {user.name}</h1>
        
        {/* Conditional rendering without architectural patterns */}
        {hasPermission('view:metrics') && (
          <MetricsPanel metrics={dashboardState.metrics || []} />
        )}
        
        <div className="dashboard-grid">
          <div className="left-column">
            <ActivityFeed 
              activities={dashboardState.activities || []} 
              realTimeUpdates={realTimeUpdates}
            />
            
            {hasPermission('view:projects') && (
              <RecentProjects projects={dashboardState.projects || []} />
            )}
          </div>
          
          <div className="right-column">
            {hasPermission('view:team') && (
              <TeamMembers members={dashboardState.team || []} />
            )}
            
            <NotificationsPanel notifications={dashboardState.notifications || []} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

// No memoization
export default Dashboard;

