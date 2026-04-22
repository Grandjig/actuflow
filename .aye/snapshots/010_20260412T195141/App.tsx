import { Suspense } from 'react';
import { useRoutes } from 'react-router-dom';
import { Spin } from 'antd';
import { routes } from './routes';
import { useAuthStore } from '@stores/authStore';
import { useEffect } from 'react';

function App() {
  const { checkAuth, isLoading } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const routing = useRoutes(routes);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Spin size="large" tip="Loading..." />
      </div>
    );
  }

  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center h-screen">
          <Spin size="large" />
        </div>
      }
    >
      {routing}
    </Suspense>
  );
}

export default App;
