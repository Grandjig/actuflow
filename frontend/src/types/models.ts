// Domain model types

export interface User {
  id: string;
  email: string;
  full_name: string;
  department?: string;
  job_title?: string;
  is_active: boolean;
  is_superuser: boolean;
  role?: Role;
  created_at: string;
  updated_at: string;
}

export interface Role {
  id: string;
  name: string;
  description?: string;
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
  risk_class?: string;
  branch_code?: string;
  term_years?: number;
  coverages?: Coverage[];
  created_at: string;
  updated_at: string;
}

export interface Policyholder {
  id: string;
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
  claim_type: string;
  status: string;
  claim_date: string;
  incident_date?: string;
  notification_date?: string;
  settlement_date?: string;
  claimed_amount: number;
  settlement_amount?: number;
  denial_reason?: string;
  adjuster_notes?: string;
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
  effective_date?: string;
  line_of_business?: string;
  approved_by_id?: string;
  approval_date?: string;
  approval_notes?: string;
  rejection_reason?: string;
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

export interface ModelDefinition {
  id: string;
  name: string;
  description?: string;
  model_type: string;
  line_of_business?: string;
  configuration: Record<string, any>;
  version: string;
  status: string;
  created_by_id: string;
  created_at: string;
  updated_at: string;
}

export interface CalculationRun {
  id: string;
  run_name: string;
  model_definition_id?: string;
  model_name?: string;
  assumption_set_id?: string;
  assumption_set_name?: string;
  status: string;
  trigger_type: string;
  triggered_by_id?: string;
  policy_filter?: Record<string, any>;
  parameters?: Record<string, any>;
  started_at?: string;
  completed_at?: string;
  duration_seconds?: number;
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
  base_assumption_set_id?: string;
  adjustments: Record<string, any>;
  status: string;
  created_by_id: string;
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
  related_resource_type?: string;
  related_resource_id?: string;
  completion_notes?: string;
  auto_generated: boolean;
  created_at: string;
  updated_at: string;
}

export interface ScheduledJob {
  id: string;
  name: string;
  description?: string;
  job_type: string;
  cron_expression: string;
  config: Record<string, any>;
  is_active: boolean;
  last_run?: string;
  next_run?: string;
  created_by_id: string;
  created_at: string;
  updated_at: string;
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

export interface ExperienceRecommendation {
  id: string;
  assumption_type: string;
  segment?: string;
  current_value: number;
  recommended_value: number;
  change_percent: number;
  confidence: number;
  sample_size: number;
  rationale: string;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  user_id: string;
  user_email?: string;
  action: string;
  resource_type: string;
  resource_id: string;
  old_values?: Record<string, any>;
  new_values?: Record<string, any>;
  ip_address?: string;
}
