import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { AIFeatures, QueryHistoryItem, ParsedIntent } from '@/types/ai';
import { aiApi } from '@api/ai';

interface AIState {
  isEnabled: boolean;
  features: AIFeatures['features'] | null;
  isLoading: boolean;
  queryHistory: QueryHistoryItem[];
  lastQuery: ParsedIntent | null;
  isQueryPending: boolean;

  fetchFeatures: () => Promise<void>;
  sendQuery: (query: string, context?: Record<string, unknown>) => Promise<ParsedIntent>;
  submitFeedback: (queryId: string, wasHelpful: boolean, feedbackText?: string) => Promise<void>;
  fetchQueryHistory: () => Promise<void>;
  clearLastQuery: () => void;
}

export const useAIStore = create<AIState>()(
  persist(
    (set, get) => ({
      isEnabled: true,
      features: null,
      isLoading: false,
      queryHistory: [],
      lastQuery: null,
      isQueryPending: false,

      fetchFeatures: async () => {
        set({ isLoading: true });
        try {
          const response = await aiApi.getFeatures();
          set({
            isEnabled: response.ai_enabled,
            features: response.features,
            isLoading: false,
          });
        } catch {
          set({ isEnabled: false, isLoading: false });
        }
      },

      sendQuery: async (query: string, context?: Record<string, unknown>) => {
        set({ isQueryPending: true });
        try {
          const result = await aiApi.query({ query, context });
          set({
            lastQuery: result,
            isQueryPending: false,
          });
          return result;
        } catch (error) {
          set({ isQueryPending: false });
          throw error;
        }
      },

      submitFeedback: async (queryId: string, wasHelpful: boolean, feedbackText?: string) => {
        await aiApi.submitFeedback(queryId, {
          was_helpful: wasHelpful,
          feedback_text: feedbackText,
        });
      },

      fetchQueryHistory: async () => {
        try {
          const history = await aiApi.getQueryHistory(20);
          set({ queryHistory: history });
        } catch {
          // Ignore
        }
      },

      clearLastQuery: () => {
        set({ lastQuery: null });
      },
    }),
    {
      name: 'actuflow-ai',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        isEnabled: state.isEnabled,
      }),
    }
  )
);
