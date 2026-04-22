// Status colors for badges
export const STATUS_COLORS: Record<string, string> = {
  // General
  active: 'green',
  inactive: 'default',
  pending: 'gold',
  
  // Policy statuses
  lapsed: 'red',
  surrendered: 'orange',
  matured: 'blue',
  claimed: 'purple',
  
  // Claim statuses
  open: 'blue',
  under_review: 'gold',
  approved: 'green',
  denied: 'red',
  paid: 'cyan',
  
  // Assumption statuses
  draft: 'default',
  pending_approval: 'gold',
  archived: 'default',
  rejected: 'red',
  
  // Calculation statuses
  queued: 'default',
  running: 'processing',
  completed: 'green',
  failed: 'red',
  cancelled: 'default',
  
  // Task statuses
  todo: 'default',
  in_progress: 'blue',
  done: 'green',
  blocked: 'red',
  
  // Priority
  urgent: 'red',
  high: 'orange',
  medium: 'blue',
  low: 'default',
};

// Product types
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
  { label: 'Long Term Care', value: 'long_term_care' },
];

// Policy statuses
export const POLICY_STATUSES = [
  { label: 'Active', value: 'active' },
  { label: 'Pending', value: 'pending' },
  { label: 'Lapsed', value: 'lapsed' },
  { label: 'Surrendered', value: 'surrendered' },
  { label: 'Matured', value: 'matured' },
  { label: 'Claimed', value: 'claimed' },
  { label: 'Cancelled', value: 'cancelled' },
];

// Premium frequencies
export const PREMIUM_FREQUENCIES = [
  { label: 'Annual', value: 'annual' },
  { label: 'Semi-Annual', value: 'semi_annual' },
  { label: 'Quarterly', value: 'quarterly' },
  { label: 'Monthly', value: 'monthly' },
  { label: 'Single', value: 'single' },
];

// Claim statuses
export const CLAIM_STATUSES = [
  { label: 'Open', value: 'open' },
  { label: 'Under Review', value: 'under_review' },
  { label: 'Approved', value: 'approved' },
  { label: 'Denied', value: 'denied' },
  { label: 'Paid', value: 'paid' },
];

// Assumption statuses
export const ASSUMPTION_STATUSES = [
  { label: 'Draft', value: 'draft' },
  { label: 'Pending Approval', value: 'pending_approval' },
  { label: 'Approved', value: 'approved' },
  { label: 'Rejected', value: 'rejected' },
  { label: 'Archived', value: 'archived' },
];

// Calculation statuses
export const CALCULATION_STATUSES = [
  { label: 'Queued', value: 'queued' },
  { label: 'Running', value: 'running' },
  { label: 'Completed', value: 'completed' },
  { label: 'Failed', value: 'failed' },
  { label: 'Cancelled', value: 'cancelled' },
];

// Task statuses
export const TASK_STATUSES = [
  { label: 'To Do', value: 'todo' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
  { label: 'Blocked', value: 'blocked' },
];

// Task priorities
export const TASK_PRIORITIES = [
  { label: 'Urgent', value: 'urgent' },
  { label: 'High', value: 'high' },
  { label: 'Medium', value: 'medium' },
  { label: 'Low', value: 'low' },
];

// Gender options
export const GENDERS = [
  { label: 'Male', value: 'male' },
  { label: 'Female', value: 'female' },
  { label: 'Other', value: 'other' },
];

// Smoker status options
export const SMOKER_STATUSES = [
  { label: 'Non-Smoker', value: 'non_smoker' },
  { label: 'Smoker', value: 'smoker' },
  { label: 'Former Smoker', value: 'former_smoker' },
];

// Currencies
export const CURRENCIES = [
  { label: 'USD - US Dollar', value: 'USD' },
  { label: 'EUR - Euro', value: 'EUR' },
  { label: 'GBP - British Pound', value: 'GBP' },
  { label: 'CAD - Canadian Dollar', value: 'CAD' },
  { label: 'AUD - Australian Dollar', value: 'AUD' },
  { label: 'JPY - Japanese Yen', value: 'JPY' },
  { label: 'CHF - Swiss Franc', value: 'CHF' },
];

// Assumption table types
export const ASSUMPTION_TABLE_TYPES = [
  { label: 'Mortality', value: 'mortality' },
  { label: 'Lapse', value: 'lapse' },
  { label: 'Expense', value: 'expense' },
  { label: 'Morbidity', value: 'morbidity' },
  { label: 'Discount Rate', value: 'discount_rate' },
  { label: 'Inflation', value: 'inflation' },
  { label: 'Commission', value: 'commission' },
];

// Model types
export const MODEL_TYPES = [
  { label: 'Reserving', value: 'reserving' },
  { label: 'Pricing', value: 'pricing' },
  { label: 'Cash Flow Projection', value: 'cashflow' },
  { label: 'Valuation', value: 'valuation' },
  { label: 'Profit Testing', value: 'profit_testing' },
];

// Regulatory standards
export const REGULATORY_STANDARDS = [
  { label: 'IFRS 17', value: 'IFRS17' },
  { label: 'Solvency II', value: 'SolvencyII' },
  { label: 'US GAAP', value: 'USGAAP' },
  { label: 'LDTI', value: 'LDTI' },
];

// Scenario types
export const SCENARIO_TYPES = [
  { label: 'Deterministic', value: 'deterministic' },
  { label: 'Stochastic', value: 'stochastic' },
  { label: 'Stress Test', value: 'stress_test' },
  { label: 'Sensitivity', value: 'sensitivity' },
];

// Report output formats
export const REPORT_FORMATS = [
  { label: 'PDF', value: 'PDF' },
  { label: 'Excel', value: 'Excel' },
  { label: 'CSV', value: 'CSV' },
];

// Job types
export const JOB_TYPES = [
  { label: 'Calculation', value: 'calculation' },
  { label: 'Report', value: 'report' },
  { label: 'Import', value: 'import' },
  { label: 'Data Check', value: 'data_check' },
  { label: 'Cleanup', value: 'cleanup' },
];

// Trigger types for automation
export const TRIGGER_TYPES = [
  { label: 'Policy Status Change', value: 'policy_status_change' },
  { label: 'Calculation Complete', value: 'calculation_complete' },
  { label: 'Assumption Approved', value: 'assumption_approved' },
  { label: 'Threshold Breach', value: 'threshold_breach' },
  { label: 'Claim Filed', value: 'claim_filed' },
  { label: 'Task Overdue', value: 'task_overdue' },
];

// Action types for automation
export const ACTION_TYPES = [
  { label: 'Send Notification', value: 'send_notification' },
  { label: 'Send Email', value: 'send_email' },
  { label: 'Create Task', value: 'create_task' },
  { label: 'Run Calculation', value: 'run_calculation' },
  { label: 'Call Webhook', value: 'call_webhook' },
];
