import { get, post, put, del } from './client';
import type { PaginatedResponse, ListParams } from '@/types/api';
import type { Policyholder } from '@/types/models';

export interface PolicyholderCreate {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  smoker_status?: string;
  occupation?: string;
  occupation_class?: string;
  email?: string;
  phone?: string;
  address_line1?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
}

export interface PolicyholderUpdate extends Partial<PolicyholderCreate> {}

export const policyholdersApi = {
  list: (params?: ListParams) =>
    get<PaginatedResponse<Policyholder>>('/policyholders', params),

  get: (id: string) =>
    get<Policyholder>(`/policyholders/${id}`),

  create: (data: PolicyholderCreate) =>
    post<Policyholder>('/policyholders', data),

  update: (id: string, data: PolicyholderUpdate) =>
    put<Policyholder>(`/policyholders/${id}`, data),

  delete: (id: string) =>
    del<void>(`/policyholders/${id}`),

  getPolicies: (id: string) =>
    get<any[]>(`/policyholders/${id}/policies`),
};
