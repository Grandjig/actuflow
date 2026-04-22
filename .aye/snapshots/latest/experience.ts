import { get, post } from './client';
import type { PaginatedResponse, PaginationParams } from '@/types/api';
import type { ExperienceAnalysis, AIRecommendation } from '@/types/models';

export interface ExperienceStudyCreateData {
  name: string;
  analysis_type: string;
  study_period_start: string;
  study_period_end: string;
  parameters?: Record<string, unknown>;
  assumption_set_id?: string;
}

export const experienceApi = {
  list: (params?: PaginationParams & { analysis_type?: string }) =>
    get<PaginatedResponse<ExperienceAnalysis>>('/experience-analysis', params),

  get: (id: string) => 
    get<ExperienceAnalysis>(`/experience-analysis/${id}`),

  create: (data: ExperienceStudyCreateData) => 
    post<ExperienceAnalysis>('/experience-analysis', data),

  getRecommendations: (id: string) =>
    get<AIRecommendation[]>(`/experience-analysis/${id}/recommendations`),
};
