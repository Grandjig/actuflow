import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Layout as AntLayout } from 'antd';
import Sidebar from './Sidebar';
import Header from './Header';

const { Content } = AntLayout;

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sidebar collapsed={collapsed} />
      <AntLayout>
        <Header collapsed={collapsed} onToggle={() => setCollapsed(!collapsed)} />
        <Content style={{ margin: 24, padding: 24, background: '#fff', minHeight: 280, borderRadius: 8 }}>
          <Outlet />
        </Content>
      </AntLayout>
    </AntLayout>
  );
}
