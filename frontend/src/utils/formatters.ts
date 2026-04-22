import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

export function formatCurrency(value: number | string | null | undefined, currency = 'USD'): string {
  if (value === null || value === undefined) return '-';
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return '-';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num);
}

export function formatNumber(value: number | string | null | undefined): string {
  if (value === null || value === undefined) return '-';
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return '-';
  return new Intl.NumberFormat('en-US').format(num);
}

export function formatCompact(value: number | string | null | undefined): string {
  if (value === null || value === undefined) return '-';
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return '-';
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(num);
}

export function formatPercent(value: number | null | undefined, decimals = 2): string {
  if (value === null || value === undefined) return '-';
  return `${(value * 100).toFixed(decimals)}%`;
}

export function formatDate(value: string | Date | null | undefined): string {
  if (!value) return '-';
  return dayjs(value).format('MMM D, YYYY');
}

export function formatDateTime(value: string | Date | null | undefined): string {
  if (!value) return '-';
  return dayjs(value).format('MMM D, YYYY HH:mm');
}

export function formatRelativeTime(value: string | Date | null | undefined): string {
  if (!value) return '-';
  return dayjs(value).fromNow();
}

export function formatDuration(seconds: number | null | undefined): string {
  if (!seconds) return '-';
  if (seconds < 60) return `${seconds}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
  const hours = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  return `${hours}h ${mins}m`;
}

export function formatStatus(status: string | null | undefined): string {
  if (!status) return '-';
  return status
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function getStatusColor(status: string | null | undefined): string {
  if (!status) return 'default';
  const s = status.toLowerCase();
  
  // Success states
  if (['active', 'approved', 'completed', 'settled', 'paid', 'success'].includes(s)) {
    return 'success';
  }
  
  // Warning states
  if (['pending', 'pending_approval', 'under_review', 'processing', 'running', 'queued', 'draft'].includes(s)) {
    return 'warning';
  }
  
  // Error states
  if (['failed', 'denied', 'rejected', 'cancelled', 'error', 'lapsed', 'surrendered'].includes(s)) {
    return 'error';
  }
  
  // Info states
  if (['new', 'filed', 'open'].includes(s)) {
    return 'processing';
  }
  
  return 'default';
}
