/**
 * Experience analysis API functions.
 */

import { get, post } from './client';
import type { ExperienceAnalysis, ExperienceRecommendation } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getExperienceStudies(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<ExperienceAnalysis>> {
  return get('/experience-analysis', params);
}

export async function getExperienceStudy(
  id: string
): Promise<ExperienceAnalysis> {
  return get(`/experience-analysis/${id}`);
}

export async function runExperienceStudy(
  data: Record<string, unknown>
): Promise<ExperienceAnalysis> {
  return post('/experience-analysis', data);
}

export async function getRecommendations(
  studyId: string
): Promise<ExperienceRecommendation[]> {
  return get(`/experience-analysis/${studyId}/recommendations`);
}
