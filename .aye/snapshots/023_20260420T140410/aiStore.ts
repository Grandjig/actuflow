import { create } from 'zustand';
import type { NaturalLanguageResponse, ParsedIntent } from '@/types/ai';

interface AIState {
  // Feature flags
  isAIEnabled: boolean;
  enabledFeatures: {
    smartImport: boolean;
    naturalLanguage: boolean;
    anomalyDetection: boolean;
    narrativeGeneration: boolean;
    semanticSearch: boolean;
    documentExtraction: boolean;
  };

  // Natural language query state
  lastQuery: string | null;
  lastResponse: NaturalLanguageResponse | null;
  queryHistory: Array<{ query: string; timestamp: Date }>;
  isPending: boolean;
  error: string | null;

  // Actions
  setAIEnabled: (enabled: boolean) => void;
  setEnabledFeatures: (features: Partial<AIState['enabledFeatures']>) => void;
  setLastQuery: (query: string) => void;
  setLastResponse: (response: NaturalLanguageResponse | null) => void;
  addToHistory: (query: string) => void;
  clearHistory: () => void;
  setIsPending: (pending: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialEnabledFeatures = {
  smartImport: true,
  naturalLanguage: true,
  anomalyDetection: true,
  narrativeGeneration: true,
  semanticSearch: true,
  documentExtraction: true,
};

export const useAIStore = create<AIState>((set, get) => ({
  // Feature flags - defaults, will be overridden by API config
  isAIEnabled: import.meta.env.VITE_AI_ENABLED !== 'false',
  enabledFeatures: { ...initialEnabledFeatures },

  // Natural language query state
  lastQuery: null,
  lastResponse: null,
  queryHistory: [],
  isPending: false,
  error: null,

  // Actions
  setAIEnabled: (enabled) => set({ isAIEnabled: enabled }),

  setEnabledFeatures: (features) =>
    set((state) => ({
      enabledFeatures: { ...state.enabledFeatures, ...features },
    })),

  setLastQuery: (query) => set({ lastQuery: query }),

  setLastResponse: (response) => set({ lastResponse: response }),

  addToHistory: (query) =>
    set((state) => ({
      queryHistory: [
        { query, timestamp: new Date() },
        ...state.queryHistory.slice(0, 49), // Keep last 50 queries
      ],
    })),

  clearHistory: () => set({ queryHistory: [] }),

  setIsPending: (pending) => set({ isPending: pending }),

  setError: (error) => set({ error }),

  reset: () =>
    set({
      lastQuery: null,
      lastResponse: null,
      isPending: false,
      error: null,
    }),
}));
