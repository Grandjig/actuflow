// Status colors
export const STATUS_COLORS: Record<string, string> = {
  active: 'green',
  lapsed: 'red',
  surrendered: 'orange',
  matured: 'blue',
  claimed: 'purple',
  cancelled: 'default',
  draft: 'default',
  pending_approval: 'gold',
  approved: 'green',
  rejected: 'red',
  archived: 'default',
  queued: 'default',
  running: 'processing',
  completed: 'success',
  failed: 'error',
  submitted: 'blue',
  under_review: 'gold',
  paid: 'green',
  denied: 'red',
  todo: 'default',
  in_progress: 'processing',
  blocked: 'error',
};

// Policy statuses
export const POLICY_STATUSES = [
  { label: 'Active', value: 'active' },
  { label: 'Lapsed', value: 'lapsed' },
  { label: 'Surrendered', value: 'surrendered' },
  { label: 'Matured', value: 'matured' },
  { label: 'Claimed', value: 'claimed' },
  { label: 'Cancelled', value: 'cancelled' },
];

// Product types
export const PRODUCT_TYPES = [
  { label: 'Term Life', value: 'term_life' },
  { label: 'Whole Life', value: 'whole_life' },
  { label: 'Universal Life', value: 'universal_life' },
  { label: 'Endowment', value: 'endowment' },
  { label: 'Annuity', value: 'annuity' },
];

// Calculation statuses
export const CALCULATION_STATUSES = [
  { label: 'Queued', value: 'queued' },
  { label: 'Running', value: 'running' },
  { label: 'Completed', value: 'completed' },
  { label: 'Failed', value: 'failed' },
  { label: 'Cancelled', value: 'cancelled' },
];

// Assumption statuses
export const ASSUMPTION_STATUSES = [
  { label: 'Draft', value: 'draft' },
  { label: 'Pending Approval', value: 'pending_approval' },
  { label: 'Approved', value: 'approved' },
  { label: 'Rejected', value: 'rejected' },
  { label: 'Archived', value: 'archived' },
];

// Claim types
export const CLAIM_TYPES = [
  { label: 'Death', value: 'death' },
  { label: 'Disability', value: 'disability' },
  { label: 'Hospitalization', value: 'hospitalization' },
  { label: 'Accident', value: 'accident' },
  { label: 'Maturity', value: 'maturity' },
  { label: 'Surrender', value: 'surrender' },
];

// Claim statuses
export const CLAIM_STATUSES = [
  { label: 'Submitted', value: 'submitted' },
  { label: 'Under Review', value: 'under_review' },
  { label: 'Approved', value: 'approved' },
  { label: 'Denied', value: 'denied' },
  { label: 'Paid', value: 'paid' },
  { label: 'Closed', value: 'closed' },
];

// Task priorities
export const TASK_PRIORITIES = [
  { label: 'Urgent', value: 'urgent', color: 'red' },
  { label: 'High', value: 'high', color: 'orange' },
  { label: 'Medium', value: 'medium', color: 'blue' },
  { label: 'Low', value: 'low', color: 'default' },
];

// Task statuses
export const TASK_STATUSES = [
  { label: 'To Do', value: 'todo' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
  { label: 'Blocked', value: 'blocked' },
];

// Premium frequencies
export const PREMIUM_FREQUENCIES = [
  { label: 'Monthly', value: 'monthly' },
  { label: 'Quarterly', value: 'quarterly' },
  { label: 'Semi-Annual', value: 'semi-annual' },
  { label: 'Annual', value: 'annual' },
  { label: 'Single', value: 'single' },
];

// Currencies
export const CURRENCIES = [
  { label: 'USD', value: 'USD' },
  { label: 'EUR', value: 'EUR' },
  { label: 'GBP', value: 'GBP' },
  { label: 'CAD', value: 'CAD' },
  { label: 'AUD', value: 'AUD' },
];

// Gender options
export const GENDERS = [
  { label: 'Male', value: 'male' },
  { label: 'Female', value: 'female' },
  { label: 'Other', value: 'other' },
];

// Smoker status
export const SMOKER_STATUSES = [
  { label: 'Non-Smoker', value: 'non_smoker' },
  { label: 'Smoker', value: 'smoker' },
  { label: 'Ex-Smoker', value: 'ex_smoker' },
  { label: 'Unknown', value: 'unknown' },
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
  { label: 'Cash Flow', value: 'cashflow' },
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

// Report types
export const REPORT_TYPES = [
  { label: 'Valuation', value: 'valuation' },
  { label: 'Regulatory', value: 'regulatory' },
  { label: 'Management', value: 'management' },
  { label: 'Ad Hoc', value: 'ad_hoc' },
];

// Job types
export const JOB_TYPES = [
  { label: 'Calculation', value: 'calculation' },
  { label: 'Report', value: 'report' },
  { label: 'Import', value: 'import' },
  { label: 'Data Check', value: 'data_check' },
  { label: 'Cleanup', value: 'cleanup' },
];

// Date formats
export const DATE_FORMAT = 'YYYY-MM-DD';
export const DATETIME_FORMAT = 'YYYY-MM-DD HH:mm:ss';
export const DISPLAY_DATE_FORMAT = 'MMM D, YYYY';
export const DISPLAY_DATETIME_FORMAT = 'MMM D, YYYY h:mm A';
