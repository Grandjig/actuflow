import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Space, Typography, Breadcrumb } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import type { BreadcrumbItem } from '@/types/ui';

const { Title } = Typography;

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumb?: BreadcrumbItem[];
  backUrl?: string;
  extra?: ReactNode;
}

export default function PageHeader({
  title,
  subtitle,
  breadcrumb,
  backUrl,
  extra,
}: PageHeaderProps) {
  const navigate = useNavigate();

  return (
    <div style={{ marginBottom: 24 }}>
      {breadcrumb && breadcrumb.length > 0 && (
        <Breadcrumb
          style={{ marginBottom: 8 }}
          items={breadcrumb.map((item) => ({
            title: item.path ? (
              <a onClick={() => navigate(item.path!)}>{item.title}</a>
            ) : (
              item.title
            ),
          }))}
        />
      )}

      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {backUrl && (
            <Button
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate(backUrl)}
            />
          )}
          <div>
            <Title level={4} style={{ margin: 0 }}>
              {title}
            </Title>
            {subtitle && (
              <Typography.Text type="secondary">{subtitle}</Typography.Text>
            )}
          </div>
        </div>

        {extra && <Space>{extra}</Space>}
      </div>
    </div>
  );
}
