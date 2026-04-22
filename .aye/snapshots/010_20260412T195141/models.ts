// Core entity types

export interface User {
  id: string;
  email: string;
  full_name: string;
  role_id: string;
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
  permissions: Permission[];
}

export interface Permission {
  id: string;
  resource: string;
  action: string;
}

export interface Policy {
  id: string;
  policy_number: string;
  product_type: ProductType;
  product_code: string;
  product_name?: string;
  status: PolicyStatus;
  policyholder_id: string;
  policyholder?: Policyholder;
  issue_date: string;
  effective_date: string;
  maturity_date?: string;
  sum_assured: number;
  premium_amount: number;
  premium_frequency: PremiumFrequency;
  currency: string;
  created_at: string;
  updated_at: string;
}

export type ProductType = 'life' | 'health' | 'property' | 'casualty';
export type PolicyStatus = 'active' | 'lapsed' | 'surrendered' | 'matured' | 'claimed';
export type PremiumFrequency = 'single' | 'monthly' | 'quarterly' | 'semi_annual' | 'annual';

export interface Policyholder {
  id: string;
  first_name: string;
  last_name: string;
  full_name: string;
  date_of_birth: string;
  age: number;
  gender: Gender;
  email?: string;
  phone?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  smoker_status: SmokerStatus;
  occupation?: string;
  created_at: string;
  updated_at: string;
}

export type Gender = 'male' | 'female' | 'other';
export type SmokerStatus = 'smoker' | 'non_smoker' | 'unknown';

export interface Coverage {
  id: string;
  policy_id: string;
  coverage_type: string;
  benefit_amount: number;
  start_date: string;
  end_date?: string;
  is_rider: boolean;
  premium_allocation: number;
}

export interface Claim {
  id: string;
  claim_number: string;
  policy_id: string;
  policy?: Policy;
  claim_type: ClaimType;
  claim_date: string;
  notification_date: string;
  claimed_amount: number;
  settlement_amount?: number;
  status: ClaimStatus;
  settlement_date?: string;
  adjuster_notes?: string;
  anomaly_score?: number;
  created_at: string;
  updated_at: string;
}

export type ClaimType = 'death' | 'disability' | 'hospitalization' | 'maturity' | 'surrender' | 'other';
export type ClaimStatus = 'open' | 'under_review' | 'approved' | 'denied' | 'paid' | 'closed';

export interface AssumptionSet {
  id: string;
  name: string;
  version: string;
  description?: string;
  status: AssumptionStatus;
  effective_date: string;
  approved_by_id?: string;
  approved_by?: User;
  approval_date?: string;
  line_of_business?: string;
  created_at: string;
  updated_at: string;
}

export type AssumptionStatus = 'draft' | 'pending_approval' | 'approved' | 'archived';

export interface AssumptionTable {
  id: string;
  assumption_set_id: string;
  table_type: AssumptionTableType;
  name: string;
  description?: string;
  data: Record<string, unknown>[];
  created_at: string;
  updated_at: string;
}

export type AssumptionTableType = 'mortality' | 'lapse' | 'expense' | 'morbidity' | 'discount_rate' | 'other';

export interface ModelDefinition {
  id: string;
  name: string;
  code: string;
  version: string;
  description?: string;
  model_type: ModelType;
  line_of_business?: string;
  regulatory_standard?: string;
  status: ModelStatus;
  configuration: ModelConfiguration;
  is_template: boolean;
  is_system_model: boolean;
  created_at: string;
  updated_at: string;
}

export type ModelType = 'reserving' | 'pricing' | 'cashflow' | 'valuation' | 'experience' | 'custom';
export type ModelStatus = 'draft' | 'active' | 'deprecated' | 'archived';

export interface ModelConfiguration {
  projection_months: number;
  time_step: 'monthly' | 'quarterly' | 'annual';
  nodes: ModelNode[];
  outputs: string[];
}

export interface ModelNode {
  id: string;
  type: 'input' | 'table_lookup' | 'calculation' | 'aggregation' | 'output';
  inputs?: string[];
  output?: string;
  formula?: string;
  table_type?: string;
  source?: string;
  fields?: string[];
}

export interface CalculationRun {
  id: string;
  run_name: string;
  run_number: number;
  model_definition_id: string;
  model_definition?: ModelDefinition;
  assumption_set_id: string;
  assumption_set?: AssumptionSet;
  status: CalculationStatus;
  trigger_type: 'manual' | 'scheduled' | 'automated';
  triggered_by_id?: string;
  triggered_by?: User;
  policy_filter?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
  queued_at: string;
  started_at?: string;
  completed_at?: string;
  policy_count?: number;
  progress_percent?: number;
  progress_message?: string;
  error_message?: string;
  result_summary?: Record<string, unknown>;
  ai_narrative?: string;
  created_at: string;
}

export type CalculationStatus = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface CalculationResult {
  id: string;
  calculation_run_id: string;
  policy_id: string;
  projection_month: number;
  result_type: string;
  values: Record<string, unknown>;
  anomaly_flag: boolean;
}

export interface Scenario {
  id: string;
  name: string;
  description?: string;
  scenario_type: 'deterministic' | 'stochastic';
  status: 'draft' | 'active' | 'archived';
  base_assumption_set_id: string;
  adjustments: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface ScenarioResult {
  id: string;
  scenario_id: string;
  calculation_run_id: string;
  comparison_base_run_id?: string;
  impact_summary: Record<string, unknown>;
  ai_narrative?: string;
  created_at: string;
}

export interface ReportTemplate {
  id: string;
  name: string;
  code: string;
  description?: string;
  report_type: 'regulatory' | 'internal' | 'adhoc';
  regulatory_standard?: string;
  output_format: 'pdf' | 'excel' | 'csv';
  template_config: Record<string, unknown>;
  is_system_template: boolean;
  include_ai_narrative: boolean;
  created_at: string;
  updated_at: string;
}

export interface GeneratedReport {
  id: string;
  report_template_id: string;
  report_template?: ReportTemplate;
  reporting_period_start: string;
  reporting_period_end: string;
  status: 'generating' | 'completed' | 'failed';
  file_path?: string;
  file_name?: string;
  file_size?: number;
  parameters?: Record<string, unknown>;
  ai_summary?: string;
  error_message?: string;
  generated_at?: string;
  created_at: string;
}

export interface DashboardConfig {
  id: string;
  name: string;
  description?: string;
  owner_id: string;
  is_shared: boolean;
  is_default: boolean;
  layout: DashboardLayout;
  widgets: WidgetConfig[];
  theme?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface DashboardLayout {
  columns: number;
  row_height: number;
}

export interface WidgetConfig {
  id: string;
  type: 'chart' | 'table' | 'metric' | 'list';
  title: string;
  data_source: string;
  config: Record<string, unknown>;
  position: { x: number; y: number; w: number; h: number };
}

export interface DataImport {
  id: string;
  file_name: string;
  file_path: string;
  import_type: string;
  status: 'pending' | 'validating' | 'processing' | 'completed' | 'failed';
  total_rows?: number;
  processed_rows?: number;
  success_rows?: number;
  error_rows?: number;
  error_details?: Record<string, unknown>;
  column_mapping?: Record<string, string>;
  ai_suggested_mapping?: Record<string, unknown>;
  ai_data_issues?: AIDataIssue[];
  uploaded_by_id: string;
  uploaded_by?: User;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface AIDataIssue {
  column: string;
  issue_type: 'missing' | 'outlier' | 'format' | 'inconsistent';
  description: string;
  affected_rows: number;
  suggestion?: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  task_type: string;
  status: TaskStatus;
  priority: TaskPriority;
  due_date?: string;
  assigned_to_id?: string;
  assigned_to?: User;
  assigned_by_id?: string;
  related_resource_type?: string;
  related_resource_id?: string;
  completion_notes?: string;
  auto_generated: boolean;
  is_overdue: boolean;
  created_at: string;
  updated_at: string;
}

export type TaskStatus = 'open' | 'in_progress' | 'completed' | 'cancelled';
export type TaskPriority = 'low' | 'medium' | 'high' | 'critical';

export interface Comment {
  id: string;
  content: string;
  user_id: string;
  user?: User;
  resource_type: string;
  resource_id: string;
  parent_comment_id?: string;
  is_resolved: boolean;
  created_at: string;
  updated_at: string;
}

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

export interface AuditLog {
  id: string;
  timestamp: string;
  user_id: string;
  user?: User;
  action: string;
  resource_type: string;
  resource_id?: string;
  old_values?: Record<string, unknown>;
  new_values?: Record<string, unknown>;
  ip_address?: string;
}

export interface ScheduledJob {
  id: string;
  name: string;
  description?: string;
  job_type: 'calculation' | 'report' | 'import' | 'data_check';
  cron_expression: string;
  config: Record<string, unknown>;
  is_active: boolean;
  last_run?: string;
  last_run_status?: string;
  next_run?: string;
  created_at: string;
  updated_at: string;
}

export interface JobExecution {
  id: string;
  scheduled_job_id: string;
  started_at: string;
  completed_at?: string;
  status: 'running' | 'completed' | 'failed';
  duration_seconds?: number;
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
  last_executed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: string;
  file_name: string;
  file_path: string;
  file_size?: number;
  content_type?: string;
  document_type?: string;
  related_resource_type?: string;
  related_resource_id?: string;
  extracted_text?: string;
  extracted_data?: Record<string, unknown>;
  extraction_confidence?: number;
  extraction_warnings?: string[];
  page_count?: number;
  created_at: string;
}

export interface ExperienceAnalysis {
  id: string;
  name: string;
  analysis_type: 'mortality' | 'lapse' | 'morbidity' | 'expense';
  study_period_start: string;
  study_period_end: string;
  parameters: Record<string, unknown>;
  results?: Record<string, unknown>;
  total_actual?: number;
  total_expected?: number;
  ae_ratio?: number;
  ai_recommendations?: AIRecommendation[];
  ai_narrative?: string;
  created_at: string;
}

export interface AIRecommendation {
  type: string;
  confidence: number;
  description: string;
  suggested_factor?: number;
}
