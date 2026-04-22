import { useState, useMemo } from 'react';
import { Table, Input, Space, Button, Dropdown, Tag } from 'antd';
import {
  SearchOutlined,
  FilterOutlined,
  DownloadOutlined,
  ReloadOutlined,
  MoreOutlined,
} from '@ant-design/icons';
import type { TableProps, ColumnsType, TablePaginationConfig } from 'antd/es/table';
import type { FilterValue, SorterResult } from 'antd/es/table/interface';
import { useDebounce } from '@/hooks/useDebounce';

interface DataTableProps<T> {
  columns: ColumnsType<T>;
  data: T[];
  loading?: boolean;
  total?: number;
  page?: number;
  pageSize?: number;
  onPaginationChange?: (page: number, pageSize: number) => void;
  onSearch?: (value: string) => void;
  onRefresh?: () => void;
  onExport?: () => void;
  rowKey?: string | ((record: T) => string);
  rowSelection?: TableProps<T>['rowSelection'];
  expandable?: TableProps<T>['expandable'];
  showSearch?: boolean;
  actions?: (record: T) => React.ReactNode;
}

export default function DataTable<T extends object>({
  columns,
  data,
  loading = false,
  total,
  page = 1,
  pageSize = 20,
  onPaginationChange,
  onSearch,
  onRefresh,
  onExport,
  rowKey = 'id',
  rowSelection,
  expandable,
  showSearch = true,
  actions,
}: DataTableProps<T>) {
  const [searchValue, setSearchValue] = useState('');
  const debouncedSearch = useDebounce(searchValue, 300);

  // Apply search when debounced value changes
  useMemo(() => {
    if (onSearch) {
      onSearch(debouncedSearch);
    }
  }, [debouncedSearch, onSearch]);

  const enhancedColumns = useMemo(() => {
    if (!actions) return columns;

    return [
      ...columns,
      {
        title: 'Actions',
        key: 'actions',
        width: 80,
        fixed: 'right' as const,
        render: (_: unknown, record: T) => actions(record),
      },
    ];
  }, [columns, actions]);

  const handleTableChange = (
    pagination: TablePaginationConfig,
    _filters: Record<string, FilterValue | null>,
    _sorter: SorterResult<T> | SorterResult<T>[]
  ) => {
    if (onPaginationChange && pagination.current && pagination.pageSize) {
      onPaginationChange(pagination.current, pagination.pageSize);
    }
  };

  return (
    <div className="data-table">
      {(showSearch || onRefresh || onExport) && (
        <div
          style={{
            padding: '16px',
            display: 'flex',
            justifyContent: 'space-between',
            borderBottom: '1px solid #f0f0f0',
          }}
        >
          {showSearch && (
            <Input
              placeholder="Search..."
              prefix={<SearchOutlined />}
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              style={{ maxWidth: 300 }}
              allowClear
            />
          )}

          <Space>
            {onRefresh && (
              <Button icon={<ReloadOutlined />} onClick={onRefresh}>
                Refresh
              </Button>
            )}
            {onExport && (
              <Button icon={<DownloadOutlined />} onClick={onExport}>
                Export
              </Button>
            )}
          </Space>
        </div>
      )}

      <Table<T>
        columns={enhancedColumns}
        dataSource={data}
        loading={loading}
        rowKey={rowKey}
        rowSelection={rowSelection}
        expandable={expandable}
        onChange={handleTableChange}
        pagination={
          total
            ? {
                current: page,
                pageSize: pageSize,
                total: total,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) =>
                  `${range[0]}-${range[1]} of ${total} items`,
              }
            : false
        }
        scroll={{ x: 'max-content' }}
      />
    </div>
  );
}
