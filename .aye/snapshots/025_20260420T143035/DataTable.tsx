import { Table, Input, Button, Space, Tooltip } from 'antd';
import { SearchOutlined, ReloadOutlined, SettingOutlined } from '@ant-design/icons';
import type { TableProps, ColumnsType } from 'antd/es/table';
import type { ReactNode } from 'react';

interface DataTableProps<T> extends Omit<TableProps<T>, 'columns'> {
  columns: ColumnsType<T>;
  data?: T[];
  total?: number;
  page?: number;
  pageSize?: number;
  onPaginationChange?: (page: number, pageSize: number) => void;
  onSearch?: (value: string) => void;
  onRefresh?: () => void;
  searchPlaceholder?: string;
  showSearch?: boolean;
  showRefresh?: boolean;
  actions?: (record: T) => ReactNode;
  toolbarExtra?: ReactNode;
}

export default function DataTable<T extends object>({
  columns,
  data,
  dataSource,
  total,
  page,
  pageSize,
  onPaginationChange,
  onSearch,
  onRefresh,
  searchPlaceholder = 'Search...',
  showSearch = true,
  showRefresh = true,
  actions,
  toolbarExtra,
  loading,
  pagination,
  ...restProps
}: DataTableProps<T>) {
  const tableData = data || dataSource || [];

  // Add actions column if provided
  const finalColumns = actions
    ? [
        ...columns,
        {
          key: 'actions',
          title: '',
          width: 50,
          render: (_: unknown, record: T) => actions(record),
        },
      ]
    : columns;

  // Pagination config
  const paginationConfig = pagination !== false
    ? {
        current: page,
        pageSize: pageSize,
        total: total,
        showSizeChanger: true,
        showTotal: (total: number) => `Total ${total} items`,
        onChange: onPaginationChange,
        onShowSizeChange: onPaginationChange,
        ...pagination,
      }
    : false;

  return (
    <div>
      {(showSearch || showRefresh || toolbarExtra) && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginBottom: 16,
          }}
        >
          <div>
            {showSearch && onSearch && (
              <Input
                placeholder={searchPlaceholder}
                prefix={<SearchOutlined />}
                style={{ width: 300 }}
                allowClear
                onChange={(e) => onSearch(e.target.value)}
              />
            )}
          </div>
          <Space>
            {toolbarExtra}
            {showRefresh && onRefresh && (
              <Tooltip title="Refresh">
                <Button icon={<ReloadOutlined />} onClick={onRefresh} />
              </Tooltip>
            )}
          </Space>
        </div>
      )}

      <Table<T>
        columns={finalColumns}
        dataSource={tableData}
        loading={loading}
        pagination={paginationConfig}
        rowKey="id"
        size="middle"
        scroll={{ x: 'max-content' }}
        {...restProps}
      />
    </div>
  );
}
