import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, Breadcrumb, Space, Button } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import type { BreadcrumbItem } from '@/types/ui';

const { Title, Text } = Typography;

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  backUrl?: string;
  breadcrumbs?: BreadcrumbItem[];
  breadcrumb?: BreadcrumbItem[]; // Alias for breadcrumbs
  tags?: ReactNode[];
  extra?: ReactNode;
}

export default function PageHeader({
  title,
  subtitle,
  backUrl,
  breadcrumbs,
  breadcrumb,
  tags,
  extra,
}: PageHeaderProps) {
  const navigate = useNavigate();
  const crumbs = breadcrumbs || breadcrumb || [];

  return (
    <div style={{ marginBottom: 24 }}>
      {crumbs.length > 0 && (
        <Breadcrumb
          style={{ marginBottom: 16 }}
          items={crumbs.map((item) => ({
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
        <div>
          <Space align="center" style={{ marginBottom: subtitle ? 8 : 0 }}>
            {backUrl && (
              <Button
                type="text"
                icon={<ArrowLeftOutlined />}
                onClick={() => navigate(backUrl)}
                style={{ marginRight: 8 }}
              />
            )}
            <Title level={3} style={{ margin: 0 }}>
              {title}
            </Title>
            {tags}
          </Space>
          {subtitle && (
            <Text type="secondary" style={{ display: 'block', marginLeft: backUrl ? 40 : 0 }}>
              {subtitle}
            </Text>
          )}
        </div>

        {extra && <div>{extra}</div>}
      </div>
    </div>
  );
}
