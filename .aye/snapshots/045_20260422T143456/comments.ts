import { get, post, put, del } from './client';
import type { SuccessResponse } from '@/types/api';
import type { Comment } from '@/types/models';

export interface CommentCreateData {
  content: string;
  resource_type: string;
  resource_id: string;
  parent_comment_id?: string;
}

export interface CommentThread {
  comment: Comment;
  replies: Comment[];
}

export const commentsApi = {
  list: (resourceType: string, resourceId: string) =>
    get<Comment[]>('/comments', { resource_type: resourceType, resource_id: resourceId }),

  getThreads: (resourceType: string, resourceId: string) =>
    get<CommentThread[]>('/comments/threads', { resource_type: resourceType, resource_id: resourceId }),

  create: (data: CommentCreateData) => 
    post<Comment>('/comments', data),

  update: (id: string, content: string) => 
    put<Comment>(`/comments/${id}`, { content }),

  resolve: (id: string) =>
    put<Comment>(`/comments/${id}/resolve`),

  delete: (id: string) => 
    del<SuccessResponse>(`/comments/${id}`),
};
