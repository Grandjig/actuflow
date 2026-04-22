// Core model types for ActuFlow frontend

export interface User {
  id: string;
  email: string;
  full_name: string;
  role?: Role;
  role_id?: string;
  department?: string;
  job_title?: string;
  is_active: boolean;
  is_superuser?: boolean;
  last_login?: string;
  ai_preferences?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  permissions: Permission[];
  is_system?: boolean;
}

export interface Permission {
  id: string;
  resource: string;
  action: string;
  description?: string;
}

export interface Policyholder {
  id: string;
  external_id?: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  date_of_birth: string;
  gender: string;
  smoker_status: string;
  occupation_class?: string;
  email?: string;
  phone?: string;
  city?: string;
  state?: string;
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
  status: string;
  policyholder_id: string;
  policyholder?: Policyholder;
  policyholder_name?: string;
  issue_date: string;
  effective_date: string;
  maturity_date?: string;
  termination_date?: string;
  sum_assured: number;
  premium_amount: number;
  premium_frequency: string;
  currency: string;
  risk_class?: string;
  term_years?: number;
  branch_code?: string;
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

export interface Claim {
  id: string;
  claim_number: string;
  policy_id: string;
  policy?: Policy;
  claim_date: string;
  incident_date?: string;
  notification_date?: string;
  claim_type: string;
  claimed_amount: number;
  status: string;
  settlement_date?: string;
  settlement_amount?: number;
  adjuster_id?: string;
  adjuster_notes?: string;
  denial_reason?: string;
  anomaly_score?: number;
  created_at: string;
  updated_at: string;
}

export interface AssumptionSet {
  id: string;
  name: string;
  version: string;
  description?: string;
  status: string;
  effective_date: string;
  expiry_date?: string;
  line_of_business?: string;
  approved_by_id?: string;
  approval_date?: string;
  approval_notes?: string;
  rejection_reason?: string;
  tables?: AssumptionTable[];
  table_count?: number;
  created_by_id: string;
  created_at: string;
  updated_at: string;
}

export interface AssumptionTable {
  id: string;
  assumption_set_id: string;
  table_type: string;
  name: string;
  description?: string;
  data: Record<string, any>;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ExperienceRecommendation {
  assumption_type: string;
  segment?: string;
  current_value: number;
  recommended_value: number;
  confidence: number;
  sample_size: number;
  rationale: string;
  impact?: {
    reserve_change: number;
    direction: 'increase' | 'decrease';
  };
}

export interface ModelDefinition {
  id: string;
  name: string;
  description?: string;
  model_type: string;
  line_of_business: string;
  regulatory_standard?: string;
  configuration: Record<string, any>;
  version: string;
  status: string;
  is_system_model: boolean;
  created_by_id: string;
  created_at: string;
  updated_at: string;
}

export interface CalculationRun {
  id: string;
  run_name: string;
  model_definition_id: string;
  model_definition?: ModelDefinition;
  model_name?: string;
  assumption_set_id: string;
  assumption_set?: AssumptionSet;
  assumption_set_name?: string;
  status: string;
  started_at?: string;
  completed_at?: string;
  duration_seconds?: number;
  triggered_by_id: string;
  trigger_type: string;
  policy_filter?: Record<string, any>;
  parameters?: Record<string, any>;
  policies_count?: number;
  error_message?: string;
  result_summary?: Record<string, any>;
  ai_narrative?: string;
  created_at: string;
  updated_at: string;
}

export interface Scenario {
  id: string;
  name: string;
  description?: string;
  scenario_type: string;
  base_assumption_set_id: string;
  adjustments: Record<string, any>;
  status: string;
  created_by_id: string;
  created_at: string;
  updated_at: string;
}

export interface ScenarioResult {
  id: string;
  scenario_id: string;
  calculation_run_id: string;
  results: Record<string, any>;
  comparison?: Record<string, any>;
  created_at: string;
}

export interface ReportTemplate {
  id: string;
  name: string;
  description?: string;
  report_type: string;
  regulatory_standard?: string;
  template_config: Record<string, any>;
  output_format: string;
  is_system_template: boolean;
  include_ai_narrative: boolean;
  created_at: string;
  updated_at: string;
}

export interface GeneratedReport {
  id: string;
  report_template_id: string;
  name: string;
  report_type: string;
  reporting_period_start?: string;
  reporting_period_end?: string;
  status: string;
  generated_by_id: string;
  generated_at?: string;
  file_path?: string;
  file_size?: number;
  ai_summary?: string;
  created_at: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  task_type: string;
  status: string;
  priority: string;
  assigned_to_id?: string;
  assigned_by_id?: string;
  due_date?: string;
  completed_at?: string;
  related_resource_type?: string;
  related_resource_id?: string;
  is_overdue?: boolean;
  auto_generated: boolean;
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

export interface ScheduledJob {
  id: string;
  name: string;
  description?: string;
  job_type: string;
  cron_expression: string;
  config: Record<string, any>;
  is_active: boolean;
  last_run_at?: string;
  last_run_status?: string;
  next_run_at?: string;
  notify_on_success?: boolean;
  notify_on_failure?: boolean;
  created_by_id: string;
  created_at: string;
  updated_at: string;
}

export interface JobExecution {
  id: string;
  scheduled_job_id: string;
  started_at: string;
  completed_at?: string;
  status: string;
  result_summary?: Record<string, any>;
  error_message?: string;
}

export interface AutomationRule {
  id: string;
  name: string;
  description?: string;
  trigger_type: string;
  trigger_config: Record<string, any>;
  action_type: string;
  action_config: Record<string, any>;
  is_active: boolean;
  created_by_id: string;
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: string;
  file_name: string;
  file_path: string;
  document_type: string;
  related_resource_type?: string;
  related_resource_id?: string;
  extracted_text?: string;
  extracted_data?: Record<string, any>;
  uploaded_by_id: string;
  uploaded_at: string;
}

export interface DataImport {
  id: string;
  file_name: string;
  import_type: string;
  status: string;
  total_rows?: number;
  processed_rows?: number;
  error_rows?: number;
  column_mapping?: Record<string, string>;
  ai_suggested_mapping?: Record<string, any>;
  ai_data_issues?: Record<string, any>[];
  uploaded_by_id: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface Comment {
  id: string;
  content: string;
  resource_type: string;
  resource_id: string;
  parent_comment_id?: string;
  author_id: string;
  author_name?: string;
  is_resolved: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuditLog {
  id: string;
  user_id?: string;
  user_email?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  old_values?: Record<string, any>;
  new_values?: Record<string, any>;
  ip_address?: string;
  created_at: string;
}
