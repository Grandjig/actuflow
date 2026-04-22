import { get, post, put, del } from './client';
import type { PaginatedResponse, PolicyholderFilters, SuccessResponse } from '@/types/api';
import type { Policyholder, Policy } from '@/types/models';

export interface PolicyholderCreateData {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  email?: string;
  phone?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  smoker_status: string;
  occupation?: string;
}

export interface PolicyholderUpdateData extends Partial<PolicyholderCreateData> {}

export const policyholdersApi = {
  list: (params?: PolicyholderFilters) =>
    get<PaginatedResponse<Policyholder>>('/policyholders', params),

  get: (id: string) => 
    get<Policyholder>(`/policyholders/${id}`),

  create: (data: PolicyholderCreateData) => 
    post<Policyholder>('/policyholders', data),

  update: (id: string, data: PolicyholderUpdateData) => 
    put<Policyholder>(`/policyholders/${id}`, data),

  delete: (id: string) => 
    del<SuccessResponse>(`/policyholders/${id}`),

  getPolicies: (id: string) =>
    get<Policy[]>(`/policyholders/${id}/policies`),

  search: (query: string, limit?: number) =>
    post<Policyholder[]>('/policyholders/search', { query, limit }),
};
