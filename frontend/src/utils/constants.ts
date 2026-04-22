// Application constants

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Status options
export const POLICY_STATUSES = [
  { label: 'Active', value: 'active' },
  { label: 'Lapsed', value: 'lapsed' },
  { label: 'Surrendered', value: 'surrendered' },
  { label: 'Matured', value: 'matured' },
  { label: 'Claimed', value: 'claimed' },
  { label: 'Cancelled', value: 'cancelled' },
];

export const CLAIM_STATUSES = [
  { label: 'Filed', value: 'filed' },
  { label: 'Under Review', value: 'under_review' },
  { label: 'Approved', value: 'approved' },
  { label: 'Denied', value: 'denied' },
  { label: 'Settled', value: 'settled' },
  { label: 'Closed', value: 'closed' },
];

export const CLAIM_TYPES = [
  { label: 'Death', value: 'death' },
  { label: 'Disability', value: 'disability' },
  { label: 'Critical Illness', value: 'critical_illness' },
  { label: 'Hospitalization', value: 'hospitalization' },
  { label: 'Accident', value: 'accident' },
  { label: 'Maturity', value: 'maturity' },
  { label: 'Surrender', value: 'surrender' },
];

export const ASSUMPTION_STATUSES = [
  { label: 'Draft', value: 'draft' },
  { label: 'Pending Approval', value: 'pending_approval' },
  { label: 'Approved', value: 'approved' },
  { label: 'Rejected', value: 'rejected' },
  { label: 'Archived', value: 'archived' },
];

export const CALCULATION_STATUSES = [
  { label: 'Queued', value: 'queued' },
  { label: 'Running', value: 'running' },
  { label: 'Completed', value: 'completed' },
  { label: 'Failed', value: 'failed' },
  { label: 'Cancelled', value: 'cancelled' },
];

export const PRODUCT_TYPES = [
  { label: 'Term Life', value: 'term_life' },
  { label: 'Whole Life', value: 'whole_life' },
  { label: 'Universal Life', value: 'universal_life' },
  { label: 'Variable Life', value: 'variable_life' },
  { label: 'Endowment', value: 'endowment' },
  { label: 'Annuity', value: 'annuity' },
  { label: 'Health', value: 'health' },
  { label: 'Disability', value: 'disability' },
  { label: 'Critical Illness', value: 'critical_illness' },
];

export const PREMIUM_FREQUENCIES = [
  { label: 'Annual', value: 'annual' },
  { label: 'Semi-Annual', value: 'semi_annual' },
  { label: 'Quarterly', value: 'quarterly' },
  { label: 'Monthly', value: 'monthly' },
  { label: 'Single', value: 'single' },
];

export const CURRENCIES = [
  { label: 'USD', value: 'USD' },
  { label: 'EUR', value: 'EUR' },
  { label: 'GBP', value: 'GBP' },
  { label: 'JPY', value: 'JPY' },
  { label: 'CAD', value: 'CAD' },
  { label: 'AUD', value: 'AUD' },
];

export const GENDERS = [
  { label: 'Male', value: 'male' },
  { label: 'Female', value: 'female' },
];

export const SMOKER_STATUSES = [
  { label: 'Non-Smoker', value: 'non_smoker' },
  { label: 'Smoker', value: 'smoker' },
  { label: 'Unknown', value: 'unknown' },
];

export const TABLE_TYPES = [
  { label: 'Mortality', value: 'mortality' },
  { label: 'Lapse', value: 'lapse' },
  { label: 'Morbidity', value: 'morbidity' },
  { label: 'Expense', value: 'expense' },
  { label: 'Discount Rate', value: 'discount_rate' },
  { label: 'Inflation', value: 'inflation' },
];

export const JOB_TYPES = [
  { label: 'Calculation', value: 'calculation' },
  { label: 'Report Generation', value: 'report' },
  { label: 'Data Import', value: 'import' },
  { label: 'Data Export', value: 'export' },
  { label: 'Data Quality Check', value: 'data_check' },
];

export const TRIGGER_TYPES = [
  { label: 'Policy Status Change', value: 'policy_status_change' },
  { label: 'Claim Filed', value: 'claim_filed' },
  { label: 'Calculation Complete', value: 'calculation_complete' },
  { label: 'Threshold Breach', value: 'threshold_breach' },
  { label: 'Data Import Complete', value: 'import_complete' },
];

export const ACTION_TYPES = [
  { label: 'Send Notification', value: 'send_notification' },
  { label: 'Create Task', value: 'create_task' },
  { label: 'Run Calculation', value: 'run_calculation' },
  { label: 'Call Webhook', value: 'call_webhook' },
  { label: 'Send Email', value: 'send_email' },
];

// Status color mappings
export const STATUS_COLORS: Record<string, string> = {
  // Policy statuses
  active: 'green',
  lapsed: 'red',
  surrendered: 'orange',
  matured: 'blue',
  claimed: 'purple',
  cancelled: 'default',

  // Claim statuses
  filed: 'blue',
  under_review: 'processing',
  approved: 'green',
  denied: 'red',
  settled: 'cyan',
  closed: 'default',

  // Assumption statuses
  draft: 'default',
  pending_approval: 'processing',
  rejected: 'red',
  archived: 'default',

  // Calculation statuses
  queued: 'default',
  running: 'processing',
  completed: 'green',
  failed: 'red',

  // General
  success: 'green',
  warning: 'orange',
  error: 'red',
  info: 'blue',
};

// Pagination defaults
export const DEFAULT_PAGE_SIZE = 20;
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];
