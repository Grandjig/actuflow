import { Navigate, Outlet } from 'react-router-dom';
import type { RouteObject } from 'react-router-dom';

// Layout
import Layout from './components/common/Layout';
import ProtectedRoute from './components/common/ProtectedRoute';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';

// Policy pages
import PolicyList from './pages/policies/PolicyList';
import PolicyDetail from './pages/policies/PolicyDetail';
import PolicyCreate from './pages/policies/PolicyCreate';

// Policyholder pages
import PolicyholderList from './pages/policyholders/PolicyholderList';
import PolicyholderDetail from './pages/policyholders/PolicyholderDetail';

// Claim pages
import ClaimList from './pages/claims/ClaimList';
import ClaimDetail from './pages/claims/ClaimDetail';
import ClaimCreate from './pages/claims/ClaimCreate';

// Assumption pages
import AssumptionSetList from './pages/assumptions/AssumptionSetList';
import AssumptionSetDetail from './pages/assumptions/AssumptionSetDetail';
import AssumptionSetCreate from './pages/assumptions/AssumptionSetCreate';

// Model pages
import ModelList from './pages/models/ModelList';
import ModelDetail from './pages/models/ModelDetail';

// Calculation pages
import CalculationList from './pages/calculations/CalculationList';
import CalculationDetail from './pages/calculations/CalculationDetail';
import CalculationCreate from './pages/calculations/CalculationCreate';

// Scenario pages
import ScenarioList from './pages/scenarios/ScenarioList';
import ScenarioDetail from './pages/scenarios/ScenarioDetail';

// Report pages
import GeneratedReportList from './pages/reports/GeneratedReportList';
import ReportTemplateList from './pages/reports/ReportTemplateList';

// Dashboard pages
import DashboardList from './pages/dashboards/DashboardList';
import DashboardEditor from './pages/dashboards/DashboardEditor';

// Import pages
import ImportList from './pages/imports/ImportList';
import ImportWizard from './pages/imports/ImportWizard';

// Task pages
import TaskList from './pages/tasks/TaskList';

// Automation pages
import ScheduledJobList from './pages/automation/ScheduledJobList';
import AutomationRuleList from './pages/automation/AutomationRuleList';

// Experience pages
import ExperienceStudyList from './pages/experience/ExperienceStudyList';

// Document pages
import DocumentList from './pages/documents/DocumentList';

// Audit pages
import AuditLogList from './pages/audit/AuditLogList';

// Admin pages
import UserList from './pages/admin/UserList';
import RoleList from './pages/admin/RoleList';

export const routes: RouteObject[] = [
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <Layout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      // Policies
      {
        path: 'policies',
        children: [
          { index: true, element: <PolicyList /> },
          { path: 'new', element: <PolicyCreate /> },
          { path: ':id', element: <PolicyDetail /> },
        ],
      },
      // Policyholders
      {
        path: 'policyholders',
        children: [
          { index: true, element: <PolicyholderList /> },
          { path: ':id', element: <PolicyholderDetail /> },
        ],
      },
      // Claims
      {
        path: 'claims',
        children: [
          { index: true, element: <ClaimList /> },
          { path: 'new', element: <ClaimCreate /> },
          { path: ':id', element: <ClaimDetail /> },
        ],
      },
      // Assumptions
      {
        path: 'assumptions',
        children: [
          { index: true, element: <AssumptionSetList /> },
          { path: 'new', element: <AssumptionSetCreate /> },
          { path: ':id', element: <AssumptionSetDetail /> },
        ],
      },
      // Models
      {
        path: 'models',
        children: [
          { index: true, element: <ModelList /> },
          { path: ':id', element: <ModelDetail /> },
        ],
      },
      // Calculations
      {
        path: 'calculations',
        children: [
          { index: true, element: <CalculationList /> },
          { path: 'new', element: <CalculationCreate /> },
          { path: ':id', element: <CalculationDetail /> },
        ],
      },
      // Scenarios
      {
        path: 'scenarios',
        children: [
          { index: true, element: <ScenarioList /> },
          { path: ':id', element: <ScenarioDetail /> },
        ],
      },
      // Reports
      {
        path: 'reports',
        children: [
          { index: true, element: <GeneratedReportList /> },
          { path: 'templates', element: <ReportTemplateList /> },
        ],
      },
      // Dashboards
      {
        path: 'dashboards',
        children: [
          { index: true, element: <DashboardList /> },
          { path: ':id', element: <DashboardEditor /> },
        ],
      },
      // Imports
      {
        path: 'imports',
        children: [
          { index: true, element: <ImportList /> },
          { path: 'new', element: <ImportWizard /> },
        ],
      },
      // Tasks
      {
        path: 'tasks',
        element: <TaskList />,
      },
      // Automation
      {
        path: 'automation',
        children: [
          { path: 'jobs', element: <ScheduledJobList /> },
          { path: 'rules', element: <AutomationRuleList /> },
        ],
      },
      // Experience
      {
        path: 'experience',
        element: <ExperienceStudyList />,
      },
      // Documents
      {
        path: 'documents',
        element: <DocumentList />,
      },
      // Audit
      {
        path: 'audit',
        element: <AuditLogList />,
      },
      // Admin
      {
        path: 'admin',
        children: [
          { path: 'users', element: <UserList /> },
          { path: 'roles', element: <RoleList /> },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
];
