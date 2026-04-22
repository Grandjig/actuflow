import { RouteObject, Navigate } from 'react-router-dom';
import Layout from './components/common/Layout';
import ProtectedRoute from './components/common/ProtectedRoute';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PolicyList from './pages/policies/PolicyList';
import PolicyDetail from './pages/policies/PolicyDetail';
import PolicyCreate from './pages/policies/PolicyCreate';
import PolicyholderList from './pages/policyholders/PolicyholderList';
import PolicyholderDetail from './pages/policyholders/PolicyholderDetail';
import ClaimList from './pages/claims/ClaimList';
import ClaimDetail from './pages/claims/ClaimDetail';
import ClaimCreate from './pages/claims/ClaimCreate';
import AssumptionSetList from './pages/assumptions/AssumptionSetList';
import AssumptionSetDetail from './pages/assumptions/AssumptionSetDetail';
import AssumptionSetCreate from './pages/assumptions/AssumptionSetCreate';
import ModelList from './pages/models/ModelList';
import ModelDetail from './pages/models/ModelDetail';
import CalculationList from './pages/calculations/CalculationList';
import CalculationDetail from './pages/calculations/CalculationDetail';
import CalculationCreate from './pages/calculations/CalculationCreate';
import ScenarioList from './pages/scenarios/ScenarioList';
import ScenarioDetail from './pages/scenarios/ScenarioDetail';
import GeneratedReportList from './pages/reports/GeneratedReportList';
import ReportTemplateList from './pages/reports/ReportTemplateList';
import DashboardList from './pages/dashboards/DashboardList';
import DashboardEditor from './pages/dashboards/DashboardEditor';
import ImportList from './pages/imports/ImportList';
import ImportWizard from './pages/imports/ImportWizard';
import TaskList from './pages/tasks/TaskList';
import ScheduledJobList from './pages/automation/ScheduledJobList';
import AutomationRuleList from './pages/automation/AutomationRuleList';
import ExperienceStudyList from './pages/experience/ExperienceStudyList';
import DocumentList from './pages/documents/DocumentList';
import AuditLogList from './pages/audit/AuditLogList';
import UserList from './pages/admin/UserList';
import RoleList from './pages/admin/RoleList';
import NotFound from './pages/NotFound';

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
      { index: true, element: <Dashboard /> },
      
      // Policies
      { path: 'policies', element: <PolicyList /> },
      { path: 'policies/new', element: <PolicyCreate /> },
      { path: 'policies/:id', element: <PolicyDetail /> },
      { path: 'policies/:id/edit', element: <PolicyCreate /> },
      
      // Policyholders
      { path: 'policyholders', element: <PolicyholderList /> },
      { path: 'policyholders/:id', element: <PolicyholderDetail /> },
      
      // Claims
      { path: 'claims', element: <ClaimList /> },
      { path: 'claims/new', element: <ClaimCreate /> },
      { path: 'claims/:id', element: <ClaimDetail /> },
      
      // Assumptions
      { path: 'assumptions', element: <AssumptionSetList /> },
      { path: 'assumptions/new', element: <AssumptionSetCreate /> },
      { path: 'assumptions/:id', element: <AssumptionSetDetail /> },
      
      // Models
      { path: 'models', element: <ModelList /> },
      { path: 'models/:id', element: <ModelDetail /> },
      
      // Calculations
      { path: 'calculations', element: <CalculationList /> },
      { path: 'calculations/new', element: <CalculationCreate /> },
      { path: 'calculations/:id', element: <CalculationDetail /> },
      
      // Scenarios
      { path: 'scenarios', element: <ScenarioList /> },
      { path: 'scenarios/:id', element: <ScenarioDetail /> },
      
      // Reports
      { path: 'reports', element: <GeneratedReportList /> },
      { path: 'reports/templates', element: <ReportTemplateList /> },
      
      // Dashboards
      { path: 'dashboards', element: <DashboardList /> },
      { path: 'dashboards/:id', element: <DashboardEditor /> },
      
      // Imports
      { path: 'imports', element: <ImportList /> },
      { path: 'imports/new', element: <ImportWizard /> },
      
      // Tasks
      { path: 'tasks', element: <TaskList /> },
      
      // Automation
      { path: 'automation/jobs', element: <ScheduledJobList /> },
      { path: 'automation/rules', element: <AutomationRuleList /> },
      
      // Experience
      { path: 'experience', element: <ExperienceStudyList /> },
      
      // Documents
      { path: 'documents', element: <DocumentList /> },
      
      // Audit
      { path: 'audit', element: <AuditLogList /> },
      
      // Admin
      { path: 'admin/users', element: <UserList /> },
      { path: 'admin/roles', element: <RoleList /> },
      
      // 404
      { path: '*', element: <NotFound /> },
    ],
  },
];
