import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { PageHeader as AntPageHeader } from '@ant-design/pro-layout';
import { Breadcrumb, Space, Tag, Button } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import type { BreadcrumbItem } from '@/types/ui';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  tags?: ReactNode[];
  extra?: ReactNode;
  breadcrumb?: BreadcrumbItem[];
  breadcrumbs?: BreadcrumbItem[]; // Alias
  backUrl?: string;
  onBack?: () => void;
  children?: ReactNode;
}

export default function PageHeader({
  title,
  subtitle,
  tags,
  extra,
  breadcrumb,
  breadcrumbs,
  backUrl,
  onBack,
  children,
}: PageHeaderProps) {
  const navigate = useNavigate();
  const crumbs = breadcrumb || breadcrumbs || [];

  const handleBack = () => {
    if (onBack) {
      onBack();
    } else if (backUrl) {
      navigate(backUrl);
    } else {
      navigate(-1);
    }
  };

  const breadcrumbItems = crumbs.map((item, index) => ({
    key: index,
    title: item.path ? (
      <a onClick={() => navigate(item.path!)}>{item.title}</a>
    ) : (
      item.title
    ),
  }));

  return (
    <div style={{ marginBottom: 24 }}>
      {crumbs.length > 0 && (
        <Breadcrumb items={breadcrumbItems} style={{ marginBottom: 8 }} />
      )}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            {(backUrl || onBack) && (
              <Button
                type="text"
                icon={<ArrowLeftOutlined />}
                onClick={handleBack}
                style={{ marginLeft: -8 }}
              />
            )}
            <h1 style={{ margin: 0, fontSize: 24, fontWeight: 600 }}>{title}</h1>
            {tags && <Space>{tags}</Space>}
          </div>
          {subtitle && (
            <p style={{ margin: '4px 0 0', color: '#666', fontSize: 14 }}>
              {subtitle}
            </p>
          )}
        </div>
        {extra && <div>{extra}</div>}
      </div>
      {children}
    </div>
  );
}
