import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { NLQueryResponse } from '@/types/ai';

interface AIState {
  // Feature flags
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
    (set, get) => ({
      // Initial state
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

      // Actions
      setAIEnabled: (enabled) => set({ isAIEnabled: enabled }),

      setEnabledFeatures: (features) => set({ enabledFeatures: features }),

      setLastQuery: (query) => set({ lastQuery: query }),

      setLastResponse: (response) => set({ lastResponse: response }),

      addToHistory: (query) => {
        const { queryHistory } = get();
        // Avoid duplicates, keep last 20
        const filtered = queryHistory.filter((q) => q !== query);
        set({ queryHistory: [query, ...filtered].slice(0, 20) });
      },

      clearHistory: () => set({ queryHistory: [] }),

      setIsPending: (pending) => set({ isPending: pending }),

      setError: (error) => set({ error }),
    }),
    {
      name: 'actuflow-ai',
      partialize: (state) => ({
        queryHistory: state.queryHistory,
        enabledFeatures: state.enabledFeatures,
      }),
    }
  )
);
