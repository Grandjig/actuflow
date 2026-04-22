import { Form, Switch, Button, message, Divider, List, Alert } from 'antd';
import { useAIStore } from '@/stores/aiStore';

export default function AISettings() {
  const { isAIEnabled, enabledFeatures, setAIEnabled, setEnabledFeatures } = useAIStore();

  const features = [
    {
      key: 'natural_language',
      title: 'Natural Language Queries',
      description: 'Ask questions in plain English',
    },
    {
      key: 'anomaly_detection',
      title: 'Anomaly Detection',
      description: 'Automatically flag suspicious patterns',
    },
    {
      key: 'narrative_generation',
      title: 'Narrative Generation',
      description: 'Auto-generate report summaries',
    },
    {
      key: 'smart_import',
      title: 'Smart Data Import',
      description: 'AI-assisted column mapping',
    },
    {
      key: 'document_extraction',
      title: 'Document Extraction',
      description: 'Extract data from uploaded documents',
    },
    {
      key: 'semantic_search',
      title: 'Semantic Search',
      description: 'Search by meaning, not just keywords',
    },
  ];

  const handleFeatureToggle = (key: string, enabled: boolean) => {
    setEnabledFeatures({ ...enabledFeatures, [key]: enabled });
  };

  const handleSubmit = () => {
    message.success('AI preferences saved');
  };

  return (
    <div style={{ maxWidth: 600 }}>
      <h3>AI Features</h3>
      <p style={{ color: '#666', marginBottom: 24 }}>
        Configure AI-powered features and preferences.
      </p>

      <Alert
        message="AI features use machine learning to assist your workflow"
        description="All AI suggestions require human confirmation. Your data is processed securely."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Form layout="vertical">
        <Form.Item label="Enable AI Features">
          <Switch
            checked={isAIEnabled}
            onChange={setAIEnabled}
            checkedChildren="On"
            unCheckedChildren="Off"
          />
        </Form.Item>

        {isAIEnabled && (
          <>
            <Divider>Individual Features</Divider>

            <List
              itemLayout="horizontal"
              dataSource={features}
              renderItem={(item) => (
                <List.Item
                  actions={[
                    <Switch
                      key={item.key}
                      checked={enabledFeatures[item.key]}
                      onChange={(checked) => handleFeatureToggle(item.key, checked)}
                    />,
                  ]}
                >
                  <List.Item.Meta title={item.title} description={item.description} />
                </List.Item>
              )}
            />
          </>
        )}

        <Divider />

        <Form.Item>
          <Button type="primary" onClick={handleSubmit}>
            Save Preferences
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
