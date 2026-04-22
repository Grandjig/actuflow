import { lazy } from 'react';
import type { RouteObject } from 'react-router-dom';
import { Navigate } from 'react-router-dom';
import Layout from '@components/common/Layout';
import AuthGuard from '@components/common/AuthGuard';

// Auth pages
const Login = lazy(() => import('@pages/Login'));

// Main pages
const Dashboard = lazy(() => import('@pages/Dashboard'));
const NotFound = lazy(() => import('@pages/NotFound'));

// Policy pages
const PolicyList = lazy(() => import('@pages/policies/PolicyList'));
const PolicyDetail = lazy(() => import('@pages/policies/PolicyDetail'));
const PolicyCreate = lazy(() => import('@pages/policies/PolicyCreate'));

// Policyholder pages
const PolicyholderList = lazy(() => import('@pages/policyholders/PolicyholderList'));
const PolicyholderDetail = lazy(() => import('@pages/policyholders/PolicyholderDetail'));

// Claim pages
const ClaimList = lazy(() => import('@pages/claims/ClaimList'));
const ClaimDetail = lazy(() => import('@pages/claims/ClaimDetail'));
const ClaimCreate = lazy(() => import('@pages/claims/ClaimCreate'));

// Assumption pages
const AssumptionSetList = lazy(() => import('@pages/assumptions/AssumptionSetList'));
const AssumptionSetDetail = lazy(() => import('@pages/assumptions/AssumptionSetDetail'));
const AssumptionSetCreate = lazy(() => import('@pages/assumptions/AssumptionSetCreate'));

// Model pages
const ModelList = lazy(() => import('@pages/models/ModelList'));
const ModelDetail = lazy(() => import('@pages/models/ModelDetail'));

// Calculation pages
const CalculationList = lazy(() => import('@pages/calculations/CalculationList'));
const CalculationDetail = lazy(() => import('@pages/calculations/CalculationDetail'));
const CalculationCreate = lazy(() => import('@pages/calculations/CalculationCreate'));

// Scenario pages
const ScenarioList = lazy(() => import('@pages/scenarios/ScenarioList'));
const ScenarioDetail = lazy(() => import('@pages/scenarios/ScenarioDetail'));

// Report pages
const ReportTemplateList = lazy(() => import('@pages/reports/ReportTemplateList'));
const GeneratedReportList = lazy(() => import('@pages/reports/GeneratedReportList'));

// Dashboard builder
const DashboardList = lazy(() => import('@pages/dashboards/DashboardList'));
const DashboardBuilder = lazy(() => import('@pages/dashboards/DashboardBuilder'));

// Import pages
const ImportList = lazy(() => import('@pages/imports/ImportList'));
const ImportWizard = lazy(() => import('@pages/imports/ImportWizard'));

// Task pages
const TaskList = lazy(() => import('@pages/tasks/TaskList'));

// Automation pages
const ScheduledJobList = lazy(() => import('@pages/automation/ScheduledJobList'));
const AutomationRuleList = lazy(() => import('@pages/automation/AutomationRuleList'));

// Experience pages
const ExperienceStudyList = lazy(() => import('@pages/experience/ExperienceStudyList'));
const ExperienceStudyDetail = lazy(() => import('@pages/experience/ExperienceStudyDetail'));

// Document pages
const DocumentList = lazy(() => import('@pages/documents/DocumentList'));

// Audit pages
const AuditLogList = lazy(() => import('@pages/audit/AuditLogList'));

// Admin pages
const UserList = lazy(() => import('@pages/admin/UserList'));
const RoleList = lazy(() => import('@pages/admin/RoleList'));
const Settings = lazy(() => import('@pages/admin/Settings'));

export const routes: RouteObject[] = [
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: (
      <AuthGuard>
        <Layout />
      </AuthGuard>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
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
          { path: ':id', element: <DashboardBuilder /> },
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
      // Documents
      {
        path: 'documents',
        element: <DocumentList />,
      },
      // Automation
      {
        path: 'automation',
        children: [
          { index: true, element: <ScheduledJobList /> },
          { path: 'rules', element: <AutomationRuleList /> },
        ],
      },
      // Experience Analysis
      {
        path: 'experience',
        children: [
          { index: true, element: <ExperienceStudyList /> },
          { path: ':id', element: <ExperienceStudyDetail /> },
        ],
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
          { path: 'settings', element: <Settings /> },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
];
