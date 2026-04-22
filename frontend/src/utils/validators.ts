// Email validation
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Policy number validation
export function isValidPolicyNumber(policyNumber: string): boolean {
  // Alphanumeric with dashes, 5-20 characters
  const policyRegex = /^[A-Za-z0-9-]{5,20}$/;
  return policyRegex.test(policyNumber);
}

// Phone number validation
export function isValidPhone(phone: string): boolean {
  // Basic phone pattern - allows various formats
  const phoneRegex = /^[+]?[0-9\s-()]{10,20}$/;
  return phoneRegex.test(phone);
}

// Date validation
export function isValidDate(dateString: string): boolean {
  const date = new Date(dateString);
  return !isNaN(date.getTime());
}

export function isDateInPast(dateString: string): boolean {
  const date = new Date(dateString);
  return date < new Date();
}

export function isDateInFuture(dateString: string): boolean {
  const date = new Date(dateString);
  return date > new Date();
}

export function isDateAfter(dateString: string, afterDateString: string): boolean {
  const date = new Date(dateString);
  const afterDate = new Date(afterDateString);
  return date > afterDate;
}

// Number validation
export function isPositiveNumber(value: number): boolean {
  return typeof value === 'number' && value > 0;
}

export function isNonNegativeNumber(value: number): boolean {
  return typeof value === 'number' && value >= 0;
}

export function isInRange(value: number, min: number, max: number): boolean {
  return typeof value === 'number' && value >= min && value <= max;
}

// Currency validation
export function isValidCurrencyAmount(value: number): boolean {
  return isNonNegativeNumber(value) && Number.isFinite(value);
}

// Percentage validation (0-100)
export function isValidPercentage(value: number): boolean {
  return isInRange(value, 0, 100);
}

// Rate validation (0-1)
export function isValidRate(value: number): boolean {
  return isInRange(value, 0, 1);
}

// UUID validation
export function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}

// Required field validation
export function isNotEmpty(value: unknown): boolean {
  if (value === null || value === undefined) return false;
  if (typeof value === 'string') return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === 'object') return Object.keys(value).length > 0;
  return true;
}

// Form validation helpers
export const validationRules = {
  required: (message = 'This field is required') => ({
    required: true,
    message,
  }),
  email: (message = 'Please enter a valid email') => ({
    type: 'email' as const,
    message,
  }),
  min: (min: number, message?: string) => ({
    min,
    message: message || `Minimum ${min} characters required`,
  }),
  max: (max: number, message?: string) => ({
    max,
    message: message || `Maximum ${max} characters allowed`,
  }),
  pattern: (pattern: RegExp, message: string) => ({
    pattern,
    message,
  }),
  positiveNumber: (message = 'Must be a positive number') => ({
    validator: (_: unknown, value: number) => {
      if (value > 0) return Promise.resolve();
      return Promise.reject(new Error(message));
    },
  }),
  futureDate: (message = 'Date must be in the future') => ({
    validator: (_: unknown, value: string) => {
      if (isDateInFuture(value)) return Promise.resolve();
      return Promise.reject(new Error(message));
    },
  }),
};
