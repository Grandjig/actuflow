import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Steps,
  Upload,
  Button,
  Table,
  Select,
  Alert,
  Space,
  Progress,
  Typography,
  Tag,
  message,
  Result,
} from 'antd';
import {
  InboxOutlined,
  RobotOutlined,
  CheckCircleOutlined,
  WarningOutlined,
} from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';

const { Dragger } = Upload;
const { Text } = Typography;

interface ColumnMapping {
  sourceColumn: string;
  targetField: string;
  confidence?: number;
}

interface DataIssue {
  row: number;
  column: string;
  issue: string;
  suggestion?: string;
}

export default function ImportWizard() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [file, setFile] = useState<File | null>(null);
  const [importType, setImportType] = useState<string>('policy');
  const [columns, setColumns] = useState<string[]>([]);
  const [mappings, setMappings] = useState<ColumnMapping[]>([]);
  const [aiSuggestions, setAiSuggestions] = useState<ColumnMapping[]>([]);
  const [dataIssues, setDataIssues] = useState<DataIssue[]>([]);
  const [importProgress, setImportProgress] = useState(0);
  const [importResult, setImportResult] = useState<any>(null);

  // Target fields by import type
  const targetFields: Record<string, { label: string; value: string }[]> = {
    policy: [
      { label: 'Policy Number', value: 'policy_number' },
      { label: 'Product Type', value: 'product_type' },
      { label: 'Product Code', value: 'product_code' },
      { label: 'Status', value: 'status' },
      { label: 'Issue Date', value: 'issue_date' },
      { label: 'Sum Assured', value: 'sum_assured' },
      { label: 'Premium Amount', value: 'premium_amount' },
      { label: 'Premium Frequency', value: 'premium_frequency' },
      { label: 'Currency', value: 'currency' },
    ],
    claim: [
      { label: 'Claim Number', value: 'claim_number' },
      { label: 'Policy Number', value: 'policy_number' },
      { label: 'Claim Type', value: 'claim_type' },
      { label: 'Claim Date', value: 'claim_date' },
      { label: 'Claimed Amount', value: 'claimed_amount' },
      { label: 'Status', value: 'status' },
    ],
  };

  const handleFileUpload = async (info: any) => {
    const uploadedFile = info.file.originFileObj || info.file;
    setFile(uploadedFile);

    // Simulate parsing file headers
    const mockColumns = [
      'pol_num',
      'prod_type',
      'prod_cd',
      'sts',
      'iss_dt',
      'sum_assd',
      'prem_amt',
      'prem_freq',
      'ccy',
    ];
    setColumns(mockColumns);

    // Simulate AI suggestions
    const suggestions: ColumnMapping[] = [
      { sourceColumn: 'pol_num', targetField: 'policy_number', confidence: 0.95 },
      { sourceColumn: 'prod_type', targetField: 'product_type', confidence: 0.92 },
      { sourceColumn: 'prod_cd', targetField: 'product_code', confidence: 0.88 },
      { sourceColumn: 'sts', targetField: 'status', confidence: 0.85 },
      { sourceColumn: 'iss_dt', targetField: 'issue_date', confidence: 0.97 },
      { sourceColumn: 'sum_assd', targetField: 'sum_assured', confidence: 0.91 },
      { sourceColumn: 'prem_amt', targetField: 'premium_amount', confidence: 0.94 },
      { sourceColumn: 'prem_freq', targetField: 'premium_frequency', confidence: 0.89 },
      { sourceColumn: 'ccy', targetField: 'currency', confidence: 0.93 },
    ];
    setAiSuggestions(suggestions);
    setMappings(suggestions);

    // Simulate AI data issues
    setDataIssues([
      { row: 15, column: 'iss_dt', issue: 'Invalid date format', suggestion: 'Convert to YYYY-MM-DD' },
      { row: 23, column: 'sum_assd', issue: 'Non-numeric value', suggestion: 'Remove currency symbol' },
      { row: 45, column: 'sts', issue: 'Unknown status value', suggestion: 'Map "A" to "active"' },
    ]);

    setCurrentStep(1);
  };

  const handleMappingChange = (sourceColumn: string, targetField: string) => {
    setMappings((prev) =>
      prev.map((m) =>
        m.sourceColumn === sourceColumn ? { ...m, targetField } : m
      )
    );
  };

  const handleValidate = async () => {
    message.loading('Validating data...');
    await new Promise((r) => setTimeout(r, 1500));
    message.destroy();
    setCurrentStep(2);
  };

  const handleImport = async () => {
    setCurrentStep(3);

    // Simulate import progress
    for (let i = 0; i <= 100; i += 10) {
      await new Promise((r) => setTimeout(r, 300));
      setImportProgress(i);
    }

    setImportResult({
      total: 1000,
      imported: 997,
      errors: 3,
    });
    setCurrentStep(4);
  };

  const mappingColumns = [
    {
      key: 'sourceColumn',
      title: 'Source Column',
      dataIndex: 'sourceColumn',
    },
    {
      key: 'targetField',
      title: 'Map To',
      dataIndex: 'targetField',
      render: (value: string, record: ColumnMapping) => (
        <Select
          value={value}
          style={{ width: 200 }}
          onChange={(v) => handleMappingChange(record.sourceColumn, v)}
          options={[
            { label: '-- Skip --', value: '' },
            ...targetFields[importType],
          ]}
        />
      ),
    },
    {
      key: 'confidence',
      title: 'AI Confidence',
      dataIndex: 'confidence',
      render: (v: number) =>
        v ? (
          <Tag color={v > 0.9 ? 'green' : v > 0.8 ? 'orange' : 'red'}>
            {(v * 100).toFixed(0)}%
          </Tag>
        ) : null,
    },
  ];

  const issueColumns = [
    { key: 'row', title: 'Row', dataIndex: 'row', width: 80 },
    { key: 'column', title: 'Column', dataIndex: 'column' },
    {
      key: 'issue',
      title: 'Issue',
      dataIndex: 'issue',
      render: (v: string) => <Text type="danger">{v}</Text>,
    },
    {
      key: 'suggestion',
      title: 'AI Suggestion',
      dataIndex: 'suggestion',
      render: (v: string) =>
        v ? (
          <Space>
            <RobotOutlined />
            {v}
          </Space>
        ) : null,
    },
  ];

  const steps = [
    { title: 'Upload', description: 'Select file' },
    { title: 'Map Columns', description: 'Configure mapping' },
    { title: 'Review', description: 'Check data' },
    { title: 'Import', description: 'Processing' },
    { title: 'Complete', description: 'Done' },
  ];

  return (
    <>
      <PageHeader
        title="Import Data"
        subtitle="Import policies, claims, or other data from files"
        breadcrumbs={[
          { title: 'Imports', path: '/imports' },
          { title: 'New Import' },
        ]}
      />

      <Card>
        <Steps current={currentStep} items={steps} style={{ marginBottom: 32 }} />

        {/* Step 0: Upload */}
        {currentStep === 0 && (
          <div>
            <div style={{ marginBottom: 24 }}>
              <label>Import Type: </label>
              <Select
                value={importType}
                onChange={setImportType}
                style={{ width: 200, marginLeft: 8 }}
                options={[
                  { label: 'Policies', value: 'policy' },
                  { label: 'Claims', value: 'claim' },
                  { label: 'Policyholders', value: 'policyholder' },
                ]}
              />
            </div>

            <Dragger
              accept=".csv,.xlsx,.xls"
              onChange={handleFileUpload}
              showUploadList={false}
              beforeUpload={() => false}
            >
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">Click or drag file to upload</p>
              <p className="ant-upload-hint">Support CSV or Excel files</p>
            </Dragger>
          </div>
        )}

        {/* Step 1: Map Columns */}
        {currentStep === 1 && (
          <div>
            <Alert
              message="AI-Suggested Mappings"
              description="We've automatically detected column mappings. Review and adjust as needed."
              type="info"
              icon={<RobotOutlined />}
              showIcon
              style={{ marginBottom: 24 }}
            />

            <Table
              columns={mappingColumns}
              dataSource={mappings}
              rowKey="sourceColumn"
              pagination={false}
              style={{ marginBottom: 24 }}
            />

            <Space>
              <Button onClick={() => setCurrentStep(0)}>Back</Button>
              <Button type="primary" onClick={handleValidate}>
                Validate Data
              </Button>
            </Space>
          </div>
        )}

        {/* Step 2: Review */}
        {currentStep === 2 && (
          <div>
            {dataIssues.length > 0 && (
              <Alert
                message={`${dataIssues.length} Data Issues Found`}
                description="Review the issues below. You can proceed but these rows may fail."
                type="warning"
                icon={<WarningOutlined />}
                showIcon
                style={{ marginBottom: 24 }}
              />
            )}

            {dataIssues.length > 0 && (
              <Table
                columns={issueColumns}
                dataSource={dataIssues}
                rowKey={(r) => `${r.row}-${r.column}`}
                pagination={false}
                style={{ marginBottom: 24 }}
              />
            )}

            {dataIssues.length === 0 && (
              <Alert
                message="Data Validation Passed"
                description="No issues found. Ready to import."
                type="success"
                icon={<CheckCircleOutlined />}
                showIcon
                style={{ marginBottom: 24 }}
              />
            )}

            <Space>
              <Button onClick={() => setCurrentStep(1)}>Back</Button>
              <Button type="primary" onClick={handleImport}>
                Start Import
              </Button>
            </Space>
          </div>
        )}

        {/* Step 3: Processing */}
        {currentStep === 3 && (
          <div style={{ textAlign: 'center', padding: 48 }}>
            <Progress type="circle" percent={importProgress} />
            <div style={{ marginTop: 24 }}>
              <Text>Importing records...</Text>
            </div>
          </div>
        )}

        {/* Step 4: Complete */}
        {currentStep === 4 && importResult && (
          <Result
            status="success"
            title="Import Complete"
            subTitle={`Successfully imported ${importResult.imported} of ${importResult.total} records.`}
            extra={[
              <Button key="view" type="primary" onClick={() => navigate('/policies')}>
                View Imported Data
              </Button>,
              <Button key="new" onClick={() => setCurrentStep(0)}>
                Import More
              </Button>,
            ]}
          >
            {importResult.errors > 0 && (
              <Alert
                message={`${importResult.errors} records failed to import`}
                type="warning"
                style={{ marginTop: 16 }}
              />
            )}
          </Result>
        )}
      </Card>
    </>
  );
}
