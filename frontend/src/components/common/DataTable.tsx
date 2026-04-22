import { Table, Input, Button, Space } from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';
import type { TableProps, TablePaginationConfig } from 'antd/es/table';
import type { ReactNode } from 'react';

interface DataTableProps<T> extends Omit<TableProps<T>, 'pagination'> {
  onSearch?: (value: string) => void;
  onRefresh?: () => void;
  searchPlaceholder?: string;
  toolbarExtra?: ReactNode;
  pagination?: TablePaginationConfig | false;
}

export default function DataTable<T extends object>({
  onSearch,
  onRefresh,
  searchPlaceholder = 'Search...',
  toolbarExtra,
  pagination,
  ...tableProps
}: DataTableProps<T>) {
  return (
    <div>
      {(onSearch || onRefresh || toolbarExtra) && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginBottom: 16,
          }}
        >
          <Space>
            {onSearch && (
              <Input.Search
                placeholder={searchPlaceholder}
                allowClear
                onSearch={onSearch}
                style={{ width: 250 }}
                prefix={<SearchOutlined />}
              />
            )}
            {toolbarExtra}
          </Space>
          {onRefresh && (
            <Button icon={<ReloadOutlined />} onClick={onRefresh}>
              Refresh
            </Button>
          )}
        </div>
      )}

      <Table<T>
        {...tableProps}
        pagination={
          pagination === false
            ? false
            : {
                showSizeChanger: true,
                showTotal: (total, range) =>
                  `${range[0]}-${range[1]} of ${total} items`,
                ...pagination,
              }
        }
      />
    </div>
  );
}
