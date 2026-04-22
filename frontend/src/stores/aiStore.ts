import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { NLQueryResponse } from '@/types/ai';

interface AIState {
  // Feature toggles
  isAIEnabled: boolean;
  enabledFeatures: Record<string, boolean>;
  
  // Query state
  lastQuery: string | null;
  lastResponse: NLQueryResponse | null;
  queryHistory: string[];
  isPending: boolean;
  error: string | null;

  // Actions
  setAIEnabled: (enabled: boolean) => void;
  setEnabledFeatures: (features: Record<string, boolean>) => void;
  setLastQuery: (query: string) => void;
  setLastResponse: (response: NLQueryResponse | null) => void;
  addToHistory: (query: string) => void;
  clearHistory: () => void;
  setIsPending: (pending: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAIStore = create<AIState>()(
  persist(
    (set) => ({
      isAIEnabled: true,
      enabledFeatures: {
        natural_language: true,
        anomaly_detection: true,
        narrative_generation: true,
        smart_import: true,
        document_extraction: true,
        semantic_search: true,
      },
      lastQuery: null,
      lastResponse: null,
      queryHistory: [],
      isPending: false,
      error: null,

      setAIEnabled: (isAIEnabled) => set({ isAIEnabled }),

      setEnabledFeatures: (enabledFeatures) => set({ enabledFeatures }),

      setLastQuery: (lastQuery) => set({ lastQuery }),

      setLastResponse: (lastResponse) => set({ lastResponse }),

      addToHistory: (query) =>
        set((state) => ({
          queryHistory: [query, ...state.queryHistory.filter((q) => q !== query)].slice(0, 50),
        })),

      clearHistory: () => set({ queryHistory: [] }),

      setIsPending: (isPending) => set({ isPending }),

      setError: (error) => set({ error }),
    }),
    {
      name: 'actuflow-ai',
      partialize: (state) => ({
        isAIEnabled: state.isAIEnabled,
        enabledFeatures: state.enabledFeatures,
        queryHistory: state.queryHistory,
      }),
    }
  )
);
