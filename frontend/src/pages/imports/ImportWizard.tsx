import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Steps, Upload, Button, Table, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import PageHeader from '@/components/common/PageHeader';

export default function ImportWizard() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);

  return (
    <>
      <PageHeader title="Import Data" backUrl="/imports" />
      <Card>
        <Steps current={step} items={[
          { title: 'Upload' },
          { title: 'Map Columns' },
          { title: 'Validate' },
          { title: 'Complete' },
        ]} style={{ marginBottom: 24 }} />

        {step === 0 && (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <Upload.Dragger
              accept=".csv,.xlsx,.xls"
              beforeUpload={() => { setStep(1); return false; }}
            >
              <p><UploadOutlined style={{ fontSize: 48, color: '#1890ff' }} /></p>
              <p>Click or drag file to upload</p>
              <p style={{ color: '#999' }}>Supports CSV, Excel</p>
            </Upload.Dragger>
          </div>
        )}

        {step === 1 && (
          <div>
            <p>Column mapping step (coming soon)</p>
            <Button type="primary" onClick={() => setStep(2)}>Next</Button>
          </div>
        )}

        {step === 2 && (
          <div>
            <p>Validation step (coming soon)</p>
            <Button type="primary" onClick={() => setStep(3)}>Import</Button>
          </div>
        )}

        {step === 3 && (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <h3>Import Complete!</h3>
            <Button type="primary" onClick={() => navigate('/imports')}>Done</Button>
          </div>
        )}
      </Card>
    </>
  );
}
