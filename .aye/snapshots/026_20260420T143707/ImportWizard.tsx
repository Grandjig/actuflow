import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Steps,
  Upload,
  Button,
  Table,
  Select,
  Space,
  Alert,
  Result,
  Progress,
  Tag,
  Typography,
  Row,
  Col,
} from 'antd';
import {
  UploadOutlined,
  CheckCircleOutlined,
  RobotOutlined,
} from '@ant-design/icons';
import type { UploadFile } from 'antd/es/upload/interface';
import PageHeader from '@/components/common/PageHeader';
import DataQualityPanel from '@/components/ai/DataQualityPanel';
import type { DataQualityIssue, ColumnMappingSuggestion } from '@/types/ai';

const { Step } = Steps;
const { Dragger } = Upload;
const { Text } = Typography;

export default function ImportWizard() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [importType, setImportType] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);

  // Mock data - in real app this comes from API after upload
  const [columns] = useState([
    'policy_no', 'dob', 'gender', 'sum_insured', 'premium', 'issue_dt', 'status'
  ]);

  const [aiSuggestions] = useState<ColumnMappingSuggestion[]>([
    { source_column: 'policy_no', suggested_field: 'policy_number', confidence: 0.98, reason: 'Exact match' },
    { source_column: 'dob', suggested_field: 'date_of_birth', confidence: 0.95, reason: 'Common abbreviation' },
    { source_column: 'gender', suggested_field: 'gender', confidence: 1.0, reason: 'Exact match' },
    { source_column: 'sum_insured', suggested_field: 'sum_assured', confidence: 0.92, reason: 'Semantically similar' },
    { source_column: 'premium', suggested_field: 'premium_amount', confidence: 0.88, reason: 'Partial match' },
    { source_column: 'issue_dt', suggested_field: 'issue_date', confidence: 0.90, reason: 'Date format detected' },
    { source_column: 'status', suggested_field: 'status', confidence: 1.0, reason: 'Exact match' },
  ]);

  const [dataIssues] = useState<DataQualityIssue[]>([
    { row: 15, column: 'premium', issue_type: 'outlier', description: 'Value 999999 is unusually high', suggested_fix: 'Verify with source' },
    { row: 23, column: 'dob', issue_type: 'invalid_format', description: 'Date format not recognized', suggested_fix: 'Expected YYYY-MM-DD' },
    { column: 'gender', issue_type: 'missing', description: '3 rows have missing gender values' },
  ]);

  const [mappings, setMappings] = useState<Record<string, string>>({});

  const targetFields = [
    { label: 'Policy Number', value: 'policy_number' },
    { label: 'Date of Birth', value: 'date_of_birth' },
    { label: 'Gender', value: 'gender' },
    { label: 'Sum Assured', value: 'sum_assured' },
    { label: 'Premium Amount', value: 'premium_amount' },
    { label: 'Issue Date', value: 'issue_date' },
    { label: 'Status', value: 'status' },
    { label: '-- Skip --', value: '' },
  ];

  const applyAISuggestions = () => {
    const newMappings: Record<string, string> = {};
    aiSuggestions.forEach((s) => {
      newMappings[s.source_column] = s.suggested_field;
    });
    setMappings(newMappings);
  };

  const handleUpload = () => {
    setIsProcessing(true);
    // Simulate upload
    setTimeout(() => {
      setIsProcessing(false);
      setCurrentStep(1);
    }, 1500);
  };

  const handleValidate = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setCurrentStep(2);
    }, 2000);
  };

  const handleCommit = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setCurrentStep(3);
    }, 3000);
  };

  const renderUploadStep = () => (
    <div>
      <Row gutter={24}>
        <Col xs={24} md={12}>
          <Card title="Select Import Type" style={{ marginBottom: 16 }}>
            <Select
              style={{ width: '100%' }}
              placeholder="What are you importing?"
              value={importType}
              onChange={setImportType}
              options={[
                { label: 'Policies', value: 'policy' },
                { label: 'Policyholders', value: 'policyholder' },
                { label: 'Claims', value: 'claim' },
                { label: 'Assumption Table', value: 'assumption' },
              ]}
            />
          </Card>
        </Col>
      </Row>

      <Card title="Upload File">
        <Dragger
          fileList={fileList}
          onChange={({ fileList }) => setFileList(fileList)}
          beforeUpload={() => false}
          accept=".csv,.xlsx,.xls"
        >
          <p className="ant-upload-drag-icon">
            <UploadOutlined />
          </p>
          <p className="ant-upload-text">Click or drag file to upload</p>
          <p className="ant-upload-hint">Supports CSV, Excel (.xlsx, .xls)</p>
        </Dragger>

        <div style={{ marginTop: 24, textAlign: 'right' }}>
          <Button
            type="primary"
            onClick={handleUpload}
            disabled={!importType || fileList.length === 0}
            loading={isProcessing}
          >
            Upload & Analyze
          </Button>
        </div>
      </Card>
    </div>
  );

  const renderMappingStep = () => (
    <div>
      <Alert
        message={
          <Space>
            <RobotOutlined />
            AI has analyzed your file and suggested column mappings
          </Space>
        }
        description="Review the suggestions below and adjust if needed."
        type="info"
        showIcon={false}
        action={
          <Button size="small" onClick={applyAISuggestions}>
            Apply All Suggestions
          </Button>
        }
        style={{ marginBottom: 16 }}
      />

      <Card title="Column Mapping" style={{ marginBottom: 16 }}>
        <Table
          dataSource={columns.map((col) => {
            const suggestion = aiSuggestions.find((s) => s.source_column === col);
            return {
              key: col,
              source: col,
              suggestion,
              mapped: mappings[col] || suggestion?.suggested_field || '',
            };
          })}
          columns={[
            {
              title: 'Source Column',
              dataIndex: 'source',
              key: 'source',
            },
            {
              title: 'AI Suggestion',
              key: 'suggestion',
              render: (_: unknown, record: any) =>
                record.suggestion ? (
                  <Space>
                    <Tag color="purple">{record.suggestion.suggested_field}</Tag>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {(record.suggestion.confidence * 100).toFixed(0)}% confidence
                    </Text>
                  </Space>
                ) : (
                  <Text type="secondary">No suggestion</Text>
                ),
            },
            {
              title: 'Map To',
              key: 'mapped',
              render: (_: unknown, record: any) => (
                <Select
                  style={{ width: 200 }}
                  value={record.mapped}
                  onChange={(value) =>
                    setMappings((prev) => ({ ...prev, [record.source]: value }))
                  }
                  options={targetFields}
                />
              ),
            },
          ]}
          pagination={false}
        />
      </Card>

      <DataQualityPanel
        issues={dataIssues}
        qualityScore={0.85}
        recommendations={[
          'Review 3 rows with missing gender values',
          'Verify the high premium value in row 15',
        ]}
      />

      <div style={{ marginTop: 24, textAlign: 'right' }}>
        <Space>
          <Button onClick={() => setCurrentStep(0)}>Back</Button>
          <Button
            type="primary"
            onClick={handleValidate}
            loading={isProcessing}
          >
            Validate & Continue
          </Button>
        </Space>
      </div>
    </div>
  );

  const renderValidationStep = () => (
    <div>
      <Card>
        <Result
          status="success"
          title="Validation Passed"
          subTitle="Your data is ready to import. Review the summary below."
        />

        <Row gutter={24} style={{ marginBottom: 24 }}>
          <Col span={8}>
            <Card size="small">
              <Text type="secondary">Total Rows</Text>
              <div style={{ fontSize: 24, fontWeight: 'bold' }}>1,234</div>
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small">
              <Text type="secondary">Valid Rows</Text>
              <div style={{ fontSize: 24, fontWeight: 'bold', color: '#52c41a' }}>1,231</div>
            </Card>
          </Col>
          <Col span={8}>
            <Card size="small">
              <Text type="secondary">Rows with Errors</Text>
              <div style={{ fontSize: 24, fontWeight: 'bold', color: '#ff4d4f' }}>3</div>
            </Card>
          </Col>
        </Row>

        <Alert
          message="3 rows will be skipped due to validation errors"
          type="warning"
          showIcon
          style={{ marginBottom: 24 }}
        />

        <div style={{ textAlign: 'right' }}>
          <Space>
            <Button onClick={() => setCurrentStep(1)}>Back</Button>
            <Button
              type="primary"
              onClick={handleCommit}
              loading={isProcessing}
            >
              Import Data
            </Button>
          </Space>
        </div>
      </Card>
    </div>
  );

  const renderCompleteStep = () => (
    <Card>
      <Result
        status="success"
        title="Import Complete!"
        subTitle="1,231 records have been successfully imported."
        extra={[
          <Button type="primary" key="view" onClick={() => navigate('/policies')}>
            View Imported Data
          </Button>,
          <Button key="another" onClick={() => {
            setCurrentStep(0);
            setFileList([]);
            setImportType('');
            setMappings({});
          }}>
            Import Another File
          </Button>,
        ]}
      />
    </Card>
  );

  const steps = [
    { title: 'Upload', content: renderUploadStep() },
    { title: 'Map Columns', content: renderMappingStep() },
    { title: 'Validate', content: renderValidationStep() },
    { title: 'Complete', content: renderCompleteStep() },
  ];

  return (
    <div>
      <PageHeader
        title="Import Data"
        subtitle="Import policies, policyholders, or claims from CSV/Excel"
        backUrl="/imports"
        breadcrumb={[
          { title: 'Home', path: '/' },
          { title: 'Data Imports', path: '/imports' },
          { title: 'New Import' },
        ]}
      />

      <Card style={{ marginBottom: 24 }}>
        <Steps current={currentStep}>
          {steps.map((step) => (
            <Step key={step.title} title={step.title} />
          ))}
        </Steps>
      </Card>

      {steps[currentStep].content}
    </div>
  );
}
