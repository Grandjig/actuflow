import { createBrowserRouter, Navigate } from 'react-router-dom';
import MainLayout from '@/layouts/MainLayout';
import AuthLayout from '@/layouts/AuthLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

// Pages
import Login from '@/pages/auth/Login';
import Dashboard from '@/pages/Dashboard';
import PolicyList from '@/pages/policies/PolicyList';
import PolicyDetail from '@/pages/policies/PolicyDetail';
import PolicyCreate from '@/pages/policies/PolicyCreate';
import AssumptionSetList from '@/pages/assumptions/AssumptionSetList';
import AssumptionSetDetail from '@/pages/assumptions/AssumptionSetDetail';
import AssumptionSetCreate from '@/pages/assumptions/AssumptionSetCreate';
import CalculationList from '@/pages/calculations/CalculationList';
import CalculationDetail from '@/pages/calculations/CalculationDetail';
import CalculationCreate from '@/pages/calculations/CalculationCreate';
import NotFound from '@/pages/NotFound';

const router = createBrowserRouter([
  // Auth routes
  {
    path: '/login',
    element: <AuthLayout />,
    children: [
      { index: true, element: <Login /> },
    ],
  },

  // Protected routes
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <Dashboard /> },

      // Policies
      { path: 'policies', element: <PolicyList /> },
      { path: 'policies/new', element: <PolicyCreate /> },
      { path: 'policies/:id', element: <PolicyDetail /> },
      { path: 'policies/:id/edit', element: <PolicyCreate /> },

      // Policyholders
      { path: 'policyholders', element: <div>Policyholders List</div> },
      { path: 'policyholders/:id', element: <div>Policyholder Detail</div> },

      // Claims
      { path: 'claims', element: <div>Claims List</div> },
      { path: 'claims/:id', element: <div>Claim Detail</div> },

      // Assumptions
      { path: 'assumptions', element: <AssumptionSetList /> },
      { path: 'assumptions/new', element: <AssumptionSetCreate /> },
      { path: 'assumptions/:id', element: <AssumptionSetDetail /> },

      // Models
      { path: 'models', element: <div>Models List</div> },
      { path: 'models/:id', element: <div>Model Detail</div> },

      // Calculations
      { path: 'calculations', element: <CalculationList /> },
      { path: 'calculations/new', element: <CalculationCreate /> },
      { path: 'calculations/:id', element: <CalculationDetail /> },

      // Scenarios
      { path: 'scenarios', element: <div>Scenarios List</div> },
      { path: 'scenarios/:id', element: <div>Scenario Detail</div> },

      // Reports
      { path: 'reports', element: <div>Reports</div> },
      { path: 'reports/:id', element: <div>Report Detail</div> },

      // Imports
      { path: 'imports', element: <div>Data Imports</div> },
      { path: 'imports/:id', element: <div>Import Detail</div> },

      // Tasks
      { path: 'tasks', element: <div>Tasks</div> },
      { path: 'tasks/:id', element: <div>Task Detail</div> },

      // Settings
      { path: 'settings', element: <div>Settings</div> },
      { path: 'settings/users', element: <div>User Management</div> },
      { path: 'settings/roles', element: <div>Role Management</div> },

      // Automation
      { path: 'automation', element: <div>Automation</div> },
      { path: 'automation/jobs', element: <div>Scheduled Jobs</div> },
      { path: 'automation/rules', element: <div>Automation Rules</div> },

      // Audit
      { path: 'audit', element: <div>Audit Logs</div> },

      // Notifications
      { path: 'notifications', element: <div>All Notifications</div> },
    ],
  },

  // 404
  { path: '*', element: <NotFound /> },
]);

export default router;
