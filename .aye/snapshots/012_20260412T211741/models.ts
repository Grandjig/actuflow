// User & Auth types
export interface User {
  id: string;
  email: string;
  full_name: string;
  role_id: string | null;
  role?: Role;
  department?: string;
  is_active: boolean;
  is_superuser: boolean;
  last_login?: string;
  created_at: string;
  updated_at: string;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  is_system_role: boolean;
  permissions?: Permission[];
}

export interface Permission {
  id: string;
  resource: string;
  action: string;
  description?: string;
}

// Policyholder types
export interface Policyholder {
  id: string;
  external_id?: string;
  first_name: string;
  last_name: string;
  full_name: string;
  date_of_birth: string;
  gender: string;
  smoker_status: string;
  occupation_class?: string;
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  created_at: string;
  updated_at: string;
}

// Policy types
export interface Policy {
  id: string;
  policy_number: string;
  product_type: string;
  product_code: string;
  product_name?: string;
  status: string;
  policyholder_id: string;
  policyholder?: Policyholder;
  issue_date: string;
  effective_date: string;
  maturity_date?: string;
  termination_date?: string;
  sum_assured: number;
  premium_amount: number;
  premium_frequency: string;
  currency: string;
  branch_code?: string;
  risk_class?: string;
  coverages?: Coverage[];
  created_at: string;
  updated_at: string;
}

export interface Coverage {
  id: string;
  policy_id: string;
  coverage_type: string;
  coverage_name: string;
  benefit_amount: number;
  premium_amount: number;
  start_date: string;
  end_date?: string;
  is_rider: boolean;
}

// Claim types
export interface Claim {
  id: string;
  claim_number: string;
  policy_id: string;
  policy?: Policy;
  claim_date: string;
  notification_date?: string;
  claim_type: string;
  claimed_amount: number;
  status: string;
  settlement_date?: string;
  settlement_amount?: number;
  adjuster_notes?: string;
  denial_reason?: string;
  anomaly_score?: number;
  created_at: string;
  updated_at: string;
}

// Assumption types
export interface AssumptionSet {
  id: string;
  name: string;
  version: string;
  description?: string;
  status: string;
  effective_date?: string;
  locked: boolean;
  approved_by?: User;
  approval_date?: string;
  created_by?: User;
  created_at: string;
  updated_at: string;
}

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

// Model types
export interface ModelDefinition {
  id: string;
  name: string;
  code: string;
  description?: string;
  model_type: string;
  line_of_business?: string;
  regulatory_standard?: string;
  configuration: ModelConfiguration;
  version: string;
  status: string;
  is_system_model: boolean;
  is_template: boolean;
  created_by?: User;
  created_at: string;
  updated_at: string;
}

export interface ModelConfiguration {
  projection_months: number;
  time_step: string;
  nodes: ModelNode[];
  outputs: string[];
}

export interface ModelNode {
  id: string;
  type: string;
  formula?: string;
  inputs?: string[];
  output?: string;
}

// Calculation types
export interface CalculationRun {
  id: string;
  run_name: string;
  model_definition_id: string;
  model_definition?: ModelDefinition;
  assumption_set_id: string;
  assumption_set?: AssumptionSet;
  status: string;
  started_at?: string;
  completed_at?: string;
  duration_seconds?: number;
  triggered_by?: User;
  trigger_type: string;
  policy_filter?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
  policy_count?: number;
  error_message?: string;
  result_summary?: Record<string, unknown>;
  ai_narrative?: string;
  progress_percent?: number;
  progress_message?: string;
  created_at: string;
  updated_at: string;
}

export interface CalculationResult {
  id: string;
  calculation_run_id: string;
  policy_id: string;
  policy?: Policy;
  projection_month: number;
  result_type: string;
  values: Record<string, unknown>;
  anomaly_flag: boolean;
}

// Scenario types
export interface Scenario {
  id: string;
  name: string;
  description?: string;
  scenario_type: string;
  base_assumption_set_id?: string;
  base_assumption_set?: AssumptionSet;
  adjustments: Record<string, ScenarioAdjustment>;
  status: string;
  created_by?: User;
  created_at: string;
  updated_at: string;
}

export interface ScenarioAdjustment {
  adjustment_type: 'factor' | 'additive' | 'absolute';
  value: number;
  applies_to?: string[];
}

// Report types
export interface ReportTemplate {
  id: string;
  name: string;
  code: string;
  description?: string;
  report_type: string;
  regulatory_standard?: string;
  template_config: Record<string, unknown>;
  output_format: string;
  is_system_template: boolean;
  include_ai_narrative: boolean;
  created_at: string;
  updated_at: string;
}

export interface GeneratedReport {
  id: string;
  report_template_id: string;
  report_template?: ReportTemplate;
  file_name: string;
  reporting_period_start: string;
  reporting_period_end: string;
  status: string;
  generated_by?: User;
  generated_at?: string;
  file_path?: string;
  file_size?: number;
  parameters?: Record<string, unknown>;
  ai_summary?: string;
  created_at: string;
}

// Dashboard types
export interface DashboardConfig {
  id: string;
  name: string;
  description?: string;
  owner_id: string;
  owner?: User;
  is_shared: boolean;
  is_default: boolean;
  layout?: Record<string, unknown>;
  widgets?: WidgetConfig[];
  created_at: string;
  updated_at: string;
}

export interface WidgetConfig {
  id: string;
  type: 'metric' | 'chart' | 'table' | 'list';
  title: string;
  config: Record<string, unknown>;
  position: {
    x: number;
    y: number;
    w: number;
    h: number;
  };
}

// Import types
export interface DataImport {
  id: string;
  file_name: string;
  file_path: string;
  import_type: string;
  status: string;
  total_rows?: number;
  processed_rows?: number;
  error_rows?: number;
  error_details?: Array<{ row: number; error: string }>;
  column_mapping?: Record<string, string>;
  ai_suggested_mapping?: Record<string, unknown>;
  ai_data_issues?: Array<Record<string, unknown>>;
  uploaded_by?: User;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

// Task types
export interface Task {
  id: string;
  title: string;
  description?: string;
  task_type: string;
  status: string;
  priority: string;
  assigned_to_id?: string;
  assigned_to?: User;
  assigned_by_id?: string;
  assigned_by?: User;
  due_date?: string;
  completed_at?: string;
  related_resource_type?: string;
  related_resource_id?: string;
  completion_notes?: string;
  auto_generated: boolean;
  is_overdue?: boolean;
  created_at: string;
  updated_at: string;
}

// Notification types
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

// Audit types
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

// Automation types
export interface ScheduledJob {
  id: string;
  name: string;
  description?: string;
  job_type: string;
  cron_expression: string;
  config: Record<string, unknown>;
  is_active: boolean;
  last_run?: string;
  last_run_status?: string;
  next_run?: string;
  created_by?: User;
  created_at: string;
  updated_at: string;
}

export interface JobExecution {
  id: string;
  scheduled_job_id: string;
  started_at: string;
  completed_at?: string;
  status: string;
  result_summary?: Record<string, unknown>;
  error_message?: string;
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
  last_triggered_at?: string;
  created_by?: User;
  created_at: string;
  updated_at: string;
}

// Experience types
export interface ExperienceAnalysis {
  id: string;
  name: string;
  analysis_type: string;
  study_period_start: string;
  study_period_end: string;
  parameters?: Record<string, unknown>;
  results?: Record<string, unknown>;
  ai_recommendations?: Array<Record<string, unknown>>;
  created_by?: User;
  created_at: string;
}

// Document types
export interface Document {
  id: string;
  file_name: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  document_type: string;
  related_resource_type?: string;
  related_resource_id?: string;
  extracted_text?: string;
  extracted_data?: Record<string, unknown>;
  extraction_confidence?: number;
  uploaded_by?: User;
  uploaded_at: string;
}
