/**
 * Comments API functions.
 */

import { get, post, put, del } from './client';
import type { Comment } from '@/types/models';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export async function getComments(
  resourceType: string,
  resourceId: string
): Promise<Comment[]> {
  return get(`/comments`, { resource_type: resourceType, resource_id: resourceId });
}

export async function createComment(
  resourceType: string,
  resourceId: string,
  content: string,
  parentCommentId?: string
): Promise<Comment> {
  return post('/comments', {
    resource_type: resourceType,
    resource_id: resourceId,
    content,
    parent_comment_id: parentCommentId,
  });
}

export async function updateComment(
  id: string,
  content: string
): Promise<Comment> {
  return put(`/comments/${id}`, { content });
}

export async function deleteComment(id: string): Promise<void> {
  return del(`/comments/${id}`);
}

export async function resolveComment(id: string): Promise<Comment> {
  return put(`/comments/${id}/resolve`);
}
