import { z } from 'zod';

// Common validation schemas
export const emailSchema = z.string().email('Invalid email address');

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number');

export const policyNumberSchema = z
  .string()
  .min(1, 'Policy number is required')
  .regex(/^[A-Z0-9][A-Z0-9\-]{2,48}[A-Z0-9]$/i, 'Invalid policy number format');

export const phoneSchema = z
  .string()
  .regex(/^\+?[0-9\s\-().]{7,20}$/, 'Invalid phone number')
  .optional()
  .or(z.literal(''));

export const currencySchema = z
  .string()
  .length(3, 'Currency must be a 3-letter code')
  .regex(/^[A-Z]{3}$/, 'Invalid currency code');

export const positiveNumberSchema = z.number().positive('Must be a positive number');

export const dateSchema = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Invalid date format (YYYY-MM-DD)');

export const cronSchema = z.string().regex(
  /^(\*|([0-9]|[1-5][0-9])|\*\/[0-9]+)\s+(\*|([0-9]|1[0-9]|2[0-3])|\*\/[0-9]+)\s+(\*|([1-9]|[12][0-9]|3[01])|\*\/[0-9]+)\s+(\*|([1-9]|1[0-2])|\*\/[0-9]+)\s+(\*|[0-6]|\*\/[0-9]+)$/,
  'Invalid cron expression'
);

// Validation functions
export function isValidEmail(email: string): boolean {
  return emailSchema.safeParse(email).success;
}

export function isValidPolicyNumber(policyNumber: string): boolean {
  return policyNumberSchema.safeParse(policyNumber).success;
}

export function isValidPhone(phone: string): boolean {
  return phoneSchema.safeParse(phone).success;
}

export function isValidDate(date: string): boolean {
  return dateSchema.safeParse(date).success;
}

export function isValidCron(cron: string): boolean {
  return cronSchema.safeParse(cron).success;
}

// Form validation helpers
export function getFieldError(errors: Record<string, string[]>, field: string): string | undefined {
  return errors[field]?.[0];
}

export function hasFieldError(errors: Record<string, string[]>, field: string): boolean {
  return Boolean(errors[field]?.length);
}
