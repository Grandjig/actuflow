import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Input, Space, Table } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';
import { usePolicyholders } from '@/hooks/usePolicyholders';
import { formatDate } from '@/utils/formatters';

export default function PolicyholderList() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const { data, isLoading } = usePolicyholders({ search });

  const columns = [
    { title: 'Name', dataIndex: 'full_name', key: 'name',
      render: (_: any, r: any) => `${r.first_name} ${r.last_name}` },
    { title: 'Date of Birth', dataIndex: 'date_of_birth', key: 'dob', render: formatDate },
    { title: 'Gender', dataIndex: 'gender', key: 'gender' },
    { title: 'Email', dataIndex: 'email', key: 'email' },
    { title: 'Phone', dataIndex: 'phone', key: 'phone' },
  ];

  return (
    <>
      <PageHeader
        title="Policyholders"
        subtitle="Manage policyholder records"
        extra={<Button type="primary" icon={<PlusOutlined />}>Add Policyholder</Button>}
      />
      <Card>
        <Space style={{ marginBottom: 16 }}>
          <Input
            placeholder="Search policyholders..."
            prefix={<SearchOutlined />}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: 300 }}
          />
        </Space>
        <Table
          columns={columns}
          dataSource={data?.items || []}
          rowKey="id"
          loading={isLoading}
          onRow={(record) => ({ onClick: () => navigate(`/policyholders/${record.id}`) })}
          pagination={{ total: data?.total, pageSize: 20 }}
        />
      </Card>
    </>
  );
}
