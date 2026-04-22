/**
 * Core data models for ActuFlow frontend.
 */

// ============================================
// User & Auth
// ============================================

export interface User {
  id: string;
  email: string;
  full_name: string;
  role_id: string;
  role?: Role;
  department?: string;
  job_title?: string;
  is_active: boolean;
  last_login?: string;
  ai_preferences?: Record<string, boolean>;
  created_at: string;
  updated_at: string;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  permissions: Permission[];
  is_system_role: boolean;
}

export interface Permission {
  id: string;
  resource: string;
  action: string;
  description?: string;
}

// ============================================
// Policy & Related
// ============================================

export interface Policyholder {
  id: string;
  external_id?: string;
  first_name: string;
  last_name: string;
  full_name: string;
  date_of_birth?: string;
  gender?: string;
  smoker_status?: string;
  occupation_class?: string;
  email?: string;
  phone?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  created_at: string;
  updated_at: string;
}

export interface Policy {
  id: string;
  policy_number: string;
  product_type: string;
  product_code: string;
  product_name?: string;
  status: PolicyStatus;
  policyholder_id: string;
  policyholder?: Policyholder;
  issue_date: string;
  effective_date: string;
  maturity_date?: string;
  termination_date?: string;
  sum_assured: number;
  premium_amount: number;
  premium_frequency: string;
  premium_due_date?: string;
  currency: string;
  branch_code?: string;
  underwriter_id?: string;
  risk_class?: string;
  policy_data?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export type PolicyStatus = 
  | 'active'
  | 'lapsed'
  | 'surrendered'
  | 'matured'
  | 'claimed'
  | 'pending'
  | 'cancelled';

export interface Coverage {
  id: string;
  policy_id: string;
  coverage_type: string;
  coverage_name: string;
  benefit_amount: number;
  premium_amount?: number;
  start_date: string;
  end_date?: string;
  is_rider: boolean;
  coverage_data?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

// ============================================
// Claims
// ============================================

export interface Claim {
  id: string;
  claim_number: string;
  policy_id: string;
  policy?: Policy;
  claim_date: string;
  incident_date?: string;
  claim_type: string;
  claim_amount: number;
  status: ClaimStatus;
  settlement_date?: string;
  settlement_amount?: number;
  adjuster_id?: string;
  adjuster_notes?: string;
  denial_reason?: string;
  anomaly_score?: number;
  claim_data?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export type ClaimStatus = 
  | 'open'
  | 'under_review'
  | 'approved'
  | 'denied'
  | 'paid'
  | 'closed';

// ============================================
// Assumptions
// ============================================

export interface AssumptionSet {
  id: string;
  name: string;
  version: string;
  description?: string;
  status: AssumptionStatus;
  effective_date: string;
  expiry_date?: string;
  approved_by?: string;
  approval_date?: string;
  approval_notes?: string;
  tables?: AssumptionTable[];
  created_at: string;
  updated_at: string;
  created_by_id: string;
}

export type AssumptionStatus = 
  | 'draft'
  | 'pending_approval'
  | 'approved'
  | 'archived';

export interface AssumptionTable {
  id: string;
  assumption_set_id: string;
  table_type: string;
  name: string;
  description?: string;
  data: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

// ============================================
// Models & Calculations
// ============================================

export interface ModelDefinition {
  id: string;
  name: string;
  description?: string;
  model_type: string;
  line_of_business?: string;
  configuration: Record<string, unknown>;
  version: string;
  status: 'draft' | 'active' | 'archived';
  created_at: string;
  updated_at: string;
  created_by_id: string;
}

export interface CalculationRun {
  id: string;
  run_name: string;
  model_definition_id: string;
  model_definition?: ModelDefinition;
  assumption_set_id: string;
  assumption_set?: AssumptionSet;
  status: CalculationStatus;
  started_at?: string;
  completed_at?: string;
  duration_seconds?: number;
  triggered_by: string;
  trigger_type: 'manual' | 'scheduled' | 'automated';
  policy_filter?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
  policies_count?: number;
  error_message?: string;
  result_summary?: Record<string, unknown>;
  ai_narrative?: string;
  created_at: string;
  updated_at: string;
}

export type CalculationStatus = 
  | 'queued'
  | 'running'
  | 'completed'
  | 'failed'
  | 'cancelled';

export interface CalculationResult {
  id: string;
  calculation_run_id: string;
  policy_id: string;
  projection_month: number;
  result_type: string;
  values: Record<string, unknown>;
  anomaly_flag: boolean;
  created_at: string;
}

export interface CalculationProgress {
  run_id: string;
  status: CalculationStatus;
  progress_percent: number;
  policies_processed: number;
  policies_total: number;
  current_step?: string;
  estimated_completion?: string;
}

// ============================================
// Scenarios
// ============================================

export interface Scenario {
  id: string;
  name: string;
  description?: string;
  scenario_type: 'deterministic' | 'stochastic';
  base_assumption_set_id: string;
  base_assumption_set?: AssumptionSet;
  adjustments: ScenarioAdjustment[];
  status: 'draft' | 'active' | 'archived';
  created_at: string;
  updated_at: string;
  created_by_id: string;
}

export interface ScenarioAdjustment {
  table_type: string;
  adjustment_type: 'multiply' | 'add' | 'replace';
  value: number;
  segment_filter?: Record<string, unknown>;
}

export interface ScenarioResult {
  id: string;
  scenario_id: string;
  scenario?: Scenario;
  calculation_run_id: string;
  calculation_run?: CalculationRun;
  comparison_base_run_id?: string;
  impact_summary: Record<string, unknown>;
  ai_narrative?: string;
  created_at: string;
}

// ============================================
// Reports
// ============================================

export interface ReportTemplate {
  id: string;
  name: string;
  description?: string;
  report_type: 'regulatory' | 'internal' | 'adhoc';
  regulatory_standard?: string;
  template_config: Record<string, unknown>;
  output_format: 'PDF' | 'Excel' | 'CSV';
  is_system_template: boolean;
  include_ai_narrative: boolean;
  created_at: string;
  updated_at: string;
  created_by_id?: string;
}

export interface GeneratedReport {
  id: string;
  report_template_id: string;
  report_template?: ReportTemplate;
  name: string;
  reporting_period_start: string;
  reporting_period_end: string;
  status: 'generating' | 'completed' | 'failed';
  generated_by: string;
  generated_at: string;
  file_path?: string;
  file_size?: number;
  parameters?: Record<string, unknown>;
  ai_summary?: string;
  created_at: string;
}

// ============================================
// Automation
// ============================================

export interface ScheduledJob {
  id: string;
  name: string;
  description?: string;
  job_type: 'calculation' | 'report' | 'import' | 'data_check';
  cron_expression: string;
  config: Record<string, unknown>;
  is_active: boolean;
  last_run?: string;
  next_run?: string;
  created_at: string;
  updated_at: string;
  created_by_id: string;
}

export interface JobExecution {
  id: string;
  scheduled_job_id: string;
  scheduled_job?: ScheduledJob;
  started_at: string;
  completed_at?: string;
  status: 'running' | 'completed' | 'failed';
  result_summary?: Record<string, unknown>;
  error_message?: string;
  created_at: string;
}

export interface AutomationRule {
  id: string;
  name: string;
  description?: string;
  trigger_type: string;
  trigger_config: Record<string, unknown>;
  action_type: string;
  action_config: Record<string, unknown>;
  is_active: boolean;
  execution_count: number;
  last_executed_at?: string;
  created_at: string;
  updated_at: string;
  created_by_id: string;
}

// ============================================
// Tasks & Workflow
// ============================================

export interface Task {
  id: string;
  title: string;
  description?: string;
  task_type: string;
  status: TaskStatus;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assigned_to?: string;
  assigned_by?: string;
  due_date?: string;
  related_resource_type?: string;
  related_resource_id?: string;
  completion_notes?: string;
  auto_generated: boolean;
  created_at: string;
  updated_at: string;
}

export type TaskStatus = 
  | 'pending'
  | 'in_progress'
  | 'completed'
  | 'cancelled';

// ============================================
// AI & Analytics
// ============================================

export interface DataQualityIssue {
  column: string;
  issue_type: string;
  severity: 'error' | 'warning' | 'info';
  count: number;
  rows?: number[];
  row?: number;
  message: string;
  suggested_fix?: string;
  suggestion?: string;
}

export interface AnomalyAlert {
  id: string;
  resource_type: string;
  resource_id: string;
  anomaly_type: string;
  severity: 'low' | 'medium' | 'high';
  score: number;
  reasons?: string[];
  description: string;
  is_resolved: boolean;
  resolved_by?: string;
  resolved_at?: string;
  created_at: string;
}

export interface ExperienceRecommendation {
  id: string;
  assumption_type: string;
  segment: string;
  current_rate: number;
  actual_rate: number;
  credibility: number;
  suggested_rate: number;
  confidence: 'low' | 'medium' | 'high';
  data_points: number;
  impact?: {
    reserve_change: number;
    direction: 'increase' | 'decrease';
  };
}

export interface AIRecommendation {
  id: string;
  type: string;
  title: string;
  description: string;
  confidence: number;
  impact?: string;
  action_url?: string;
  created_at: string;
}

// ============================================
// Documents
// ============================================

export interface Document {
  id: string;
  file_name: string;
  file_path: string;
  file_size: number;
  content_type: string;
  document_type?: string;
  related_resource_type?: string;
  related_resource_id?: string;
  extracted_text?: string;
  extracted_data?: Record<string, unknown>;
  extraction_confidence?: number;
  page_count?: number;
  uploaded_by_id: string;
  created_at: string;
  updated_at: string;
}

// ============================================
// Experience Analysis
// ============================================

export interface ExperienceAnalysis {
  id: string;
  analysis_type: string;
  study_period_start: string;
  study_period_end: string;
  parameters: Record<string, unknown>;
  results: Record<string, unknown>;
  ai_recommendations?: ExperienceRecommendation[];
  status: 'running' | 'completed' | 'failed';
  created_at: string;
  created_by_id: string;
}

// ============================================
// Data Import
// ============================================

export interface DataImport {
  id: string;
  file_name: string;
  file_path: string;
  import_type: string;
  status: 'pending' | 'validating' | 'validated' | 'importing' | 'completed' | 'failed';
  total_rows: number;
  processed_rows: number;
  error_rows: number;
  error_details?: Record<string, unknown>[];
  column_mapping?: Record<string, string>;
  ai_suggested_mapping?: Record<string, string>;
  ai_data_issues?: DataQualityIssue[];
  uploaded_by_id: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

// ============================================
// Notifications
// ============================================

export interface Notification {
  id: string;
  user_id: string;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  resource_type?: string;
  resource_id?: string;
  created_at: string;
}

// ============================================
// Audit
// ============================================

export interface AuditLog {
  id: string;
  timestamp: string;
  user_id?: string;
  user?: User;
  action: string;
  resource_type: string;
  resource_id?: string;
  old_values?: Record<string, unknown>;
  new_values?: Record<string, unknown>;
  ip_address?: string;
  user_agent?: string;
}

// ============================================
// Dashboard
// ============================================

export interface DashboardConfig {
  id: string;
  name: string;
  owner_id: string;
  is_shared: boolean;
  layout: Record<string, unknown>;
  widgets: WidgetConfig[];
  created_at: string;
  updated_at: string;
}

export interface WidgetConfig {
  id: string;
  type: string;
  title: string;
  config: Record<string, unknown>;
  position: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
}
