// Status options
export const POLICY_STATUSES = [
  { label: 'Active', value: 'active' },
  { label: 'Lapsed', value: 'lapsed' },
  { label: 'Surrendered', value: 'surrendered' },
  { label: 'Matured', value: 'matured' },
  { label: 'Claimed', value: 'claimed' },
];

export const CLAIM_STATUSES = [
  { label: 'Open', value: 'open' },
  { label: 'Under Review', value: 'under_review' },
  { label: 'Approved', value: 'approved' },
  { label: 'Denied', value: 'denied' },
  { label: 'Paid', value: 'paid' },
  { label: 'Closed', value: 'closed' },
];

export const ASSUMPTION_STATUSES = [
  { label: 'Draft', value: 'draft' },
  { label: 'Pending Approval', value: 'pending_approval' },
  { label: 'Approved', value: 'approved' },
  { label: 'Archived', value: 'archived' },
];

export const CALCULATION_STATUSES = [
  { label: 'Queued', value: 'queued' },
  { label: 'Running', value: 'running' },
  { label: 'Completed', value: 'completed' },
  { label: 'Failed', value: 'failed' },
  { label: 'Cancelled', value: 'cancelled' },
];

export const TASK_STATUSES = [
  { label: 'Open', value: 'open' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' },
];

export const TASK_PRIORITIES = [
  { label: 'Low', value: 'low' },
  { label: 'Medium', value: 'medium' },
  { label: 'High', value: 'high' },
  { label: 'Critical', value: 'critical' },
];

// Type options
export const PRODUCT_TYPES = [
  { label: 'Life', value: 'life' },
  { label: 'Health', value: 'health' },
  { label: 'Property', value: 'property' },
  { label: 'Casualty', value: 'casualty' },
];

export const CLAIM_TYPES = [
  { label: 'Death', value: 'death' },
  { label: 'Disability', value: 'disability' },
  { label: 'Hospitalization', value: 'hospitalization' },
  { label: 'Maturity', value: 'maturity' },
  { label: 'Surrender', value: 'surrender' },
  { label: 'Other', value: 'other' },
];

export const PREMIUM_FREQUENCIES = [
  { label: 'Single', value: 'single' },
  { label: 'Monthly', value: 'monthly' },
  { label: 'Quarterly', value: 'quarterly' },
  { label: 'Semi-Annual', value: 'semi_annual' },
  { label: 'Annual', value: 'annual' },
];

export const GENDERS = [
  { label: 'Male', value: 'male' },
  { label: 'Female', value: 'female' },
  { label: 'Other', value: 'other' },
];

export const SMOKER_STATUSES = [
  { label: 'Non-Smoker', value: 'non_smoker' },
  { label: 'Smoker', value: 'smoker' },
  { label: 'Unknown', value: 'unknown' },
];

export const MODEL_TYPES = [
  { label: 'Reserving', value: 'reserving' },
  { label: 'Pricing', value: 'pricing' },
  { label: 'Cashflow', value: 'cashflow' },
  { label: 'Valuation', value: 'valuation' },
  { label: 'Experience', value: 'experience' },
  { label: 'Custom', value: 'custom' },
];

export const ASSUMPTION_TABLE_TYPES = [
  { label: 'Mortality', value: 'mortality' },
  { label: 'Lapse', value: 'lapse' },
  { label: 'Expense', value: 'expense' },
  { label: 'Morbidity', value: 'morbidity' },
  { label: 'Discount Rate', value: 'discount_rate' },
  { label: 'Other', value: 'other' },
];

export const JOB_TYPES = [
  { label: 'Calculation', value: 'calculation' },
  { label: 'Report', value: 'report' },
  { label: 'Import', value: 'import' },
  { label: 'Data Check', value: 'data_check' },
];

export const TRIGGER_TYPES = [
  { label: 'Policy Status Change', value: 'policy_status_change' },
  { label: 'Calculation Complete', value: 'calculation_complete' },
  { label: 'Threshold Breach', value: 'threshold_breach' },
  { label: 'Time Based', value: 'time_based' },
  { label: 'Claim Status Change', value: 'claim_status_change' },
  { label: 'Assumption Approved', value: 'assumption_approved' },
  { label: 'Import Complete', value: 'import_complete' },
];

export const ACTION_TYPES = [
  { label: 'Send Notification', value: 'send_notification' },
  { label: 'Create Task', value: 'create_task' },
  { label: 'Run Calculation', value: 'run_calculation' },
  { label: 'Call Webhook', value: 'call_webhook' },
  { label: 'Send Email', value: 'send_email' },
  { label: 'Update Status', value: 'update_status' },
];

export const EXPERIENCE_ANALYSIS_TYPES = [
  { label: 'Mortality', value: 'mortality' },
  { label: 'Lapse', value: 'lapse' },
  { label: 'Morbidity', value: 'morbidity' },
  { label: 'Expense', value: 'expense' },
];

// Currency options
export const CURRENCIES = [
  { label: 'US Dollar (USD)', value: 'USD' },
  { label: 'Euro (EUR)', value: 'EUR' },
  { label: 'British Pound (GBP)', value: 'GBP' },
  { label: 'Japanese Yen (JPY)', value: 'JPY' },
  { label: 'Canadian Dollar (CAD)', value: 'CAD' },
  { label: 'Australian Dollar (AUD)', value: 'AUD' },
  { label: 'Swiss Franc (CHF)', value: 'CHF' },
];

// Pagination
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];
export const DEFAULT_PAGE_SIZE = 20;
