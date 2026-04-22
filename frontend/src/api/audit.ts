import { get, downloadFile } from './client';
import type { PaginatedResponse, AuditLogFilters } from '@/types/api';
import type { AuditLog } from '@/types/models';

export const auditApi = {
  list: (params?: AuditLogFilters) =>
    get<PaginatedResponse<AuditLog>>('/audit-logs', params),

  export: (params?: AuditLogFilters) =>
    downloadFile('/audit-logs/export', 'audit_logs.csv'),
};
