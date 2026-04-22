import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

// Date formatting
export function formatDate(date: string | Date | undefined | null, format = 'MMM D, YYYY'): string {
  if (!date) return '-';
  return dayjs(date).format(format);
}

export function formatDateTime(date: string | Date | undefined | null): string {
  if (!date) return '-';
  return dayjs(date).format('MMM D, YYYY h:mm A');
}

export function formatRelativeTime(date: string | Date | undefined | null): string {
  if (!date) return '-';
  return dayjs(date).fromNow();
}

// Currency formatting
export function formatCurrency(
  amount: number | undefined | null,
  currency = 'USD',
  options?: Intl.NumberFormatOptions
): string {
  if (amount === null || amount === undefined) return '-';
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
    ...options,
  }).format(amount);
}

// Number formatting
export function formatNumber(
  value: number | undefined | null,
  options?: Intl.NumberFormatOptions
): string {
  if (value === null || value === undefined) return '-';
  
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
    ...options,
  }).format(value);
}

export function formatCompactNumber(value: number | undefined | null): string {
  if (value === null || value === undefined) return '-';
  
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    compactDisplay: 'short',
  }).format(value);
}

// Percentage formatting
export function formatPercent(
  value: number | undefined | null,
  decimals = 2
): string {
  if (value === null || value === undefined) return '-';
  
  // Assume value is decimal (0.05 = 5%)
  return `${(value * 100).toFixed(decimals)}%`;
}

export function formatPercentRaw(
  value: number | undefined | null,
  decimals = 2
): string {
  if (value === null || value === undefined) return '-';
  
  // Value is already percentage (5 = 5%)
  return `${value.toFixed(decimals)}%`;
}

// Duration formatting
export function formatDuration(seconds: number | undefined | null): string {
  if (!seconds) return '-';
  
  if (seconds < 60) {
    return `${seconds}s`;
  }
  
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  
  if (minutes < 60) {
    return remainingSeconds > 0 
      ? `${minutes}m ${remainingSeconds}s`
      : `${minutes}m`;
  }
  
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  
  return remainingMinutes > 0
    ? `${hours}h ${remainingMinutes}m`
    : `${hours}h`;
}

// Status formatting
export function formatStatus(status: string | undefined | null): string {
  if (!status) return '-';
  
  return status
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

// File size formatting
export function formatFileSize(bytes: number | undefined | null): string {
  if (!bytes) return '-';
  
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let unitIndex = 0;
  let size = bytes;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(1)} ${units[unitIndex]}`;
}

// Truncate text
export function truncate(text: string | undefined | null, maxLength: number): string {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}
