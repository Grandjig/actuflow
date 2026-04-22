import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Layout } from 'antd';

import Sidebar from './Sidebar';
import Header from '@/components/common/Header';
import AISearchBar from '@/components/ai/AISearchBar';
import { useUIStore } from '@/stores/uiStore';

const { Content } = Layout;

export default function MainLayout() {
  const { sidebarCollapsed } = useUIStore();
  const [searchOpen, setSearchOpen] = useState(false);

  // Global keyboard shortcut for AI search
  const handleKeyDown = (e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      setSearchOpen(true);
    }
  };

  // Register global listener
  useState(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  });

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sidebar collapsed={sidebarCollapsed} />
      <Layout>
        <Header />
        <Content
          style={{
            margin: 24,
            minHeight: 280,
          }}
        >
          <Outlet />
        </Content>
      </Layout>

      <AISearchBar open={searchOpen} onClose={() => setSearchOpen(false)} />
    </Layout>
  );
}
