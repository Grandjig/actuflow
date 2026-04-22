import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface UIState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  pageSize: number;
  recentSearches: string[];
  commandPaletteOpen: boolean;

  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setPageSize: (size: number) => void;
  addRecentSearch: (search: string) => void;
  clearRecentSearches: () => void;
  setCommandPaletteOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      sidebarCollapsed: false,
      theme: 'light',
      pageSize: 20,
      recentSearches: [],
      commandPaletteOpen: false,

      toggleSidebar: () => {
        set({ sidebarCollapsed: !get().sidebarCollapsed });
      },

      setSidebarCollapsed: (collapsed: boolean) => {
        set({ sidebarCollapsed: collapsed });
      },

      setTheme: (theme: 'light' | 'dark') => {
        set({ theme });
        document.documentElement.classList.toggle('dark', theme === 'dark');
      },

      setPageSize: (size: number) => {
        set({ pageSize: size });
      },

      addRecentSearch: (search: string) => {
        const { recentSearches } = get();
        const updated = [search, ...recentSearches.filter((s) => s !== search)].slice(0, 10);
        set({ recentSearches: updated });
      },

      clearRecentSearches: () => {
        set({ recentSearches: [] });
      },

      setCommandPaletteOpen: (open: boolean) => {
        set({ commandPaletteOpen: open });
      },
    }),
    {
      name: 'actuflow-ui',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        sidebarCollapsed: state.sidebarCollapsed,
        theme: state.theme,
        pageSize: state.pageSize,
        recentSearches: state.recentSearches,
      }),
    }
  )
);
