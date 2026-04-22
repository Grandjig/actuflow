import { Form, Switch, Button, message, Divider, List } from 'antd';

const notificationTypes = [
  {
    key: 'calculation_complete',
    title: 'Calculation Complete',
    description: 'Notify when a calculation run completes',
  },
  {
    key: 'approval_required',
    title: 'Approval Required',
    description: 'Notify when items need your approval',
  },
  {
    key: 'task_assigned',
    title: 'Task Assigned',
    description: 'Notify when a task is assigned to you',
  },
  {
    key: 'anomaly_detected',
    title: 'Anomaly Detected',
    description: 'Notify when AI detects anomalies',
  },
  {
    key: 'import_complete',
    title: 'Import Complete',
    description: 'Notify when data import finishes',
  },
];

export default function NotificationSettings() {
  const handleSubmit = () => {
    message.success('Notification preferences saved');
  };

  return (
    <div style={{ maxWidth: 600 }}>
      <h3>Notification Preferences</h3>
      <p style={{ color: '#666', marginBottom: 24 }}>
        Choose which notifications you want to receive.
      </p>

      <Form layout="vertical" onFinish={handleSubmit}>
        <List
          itemLayout="horizontal"
          dataSource={notificationTypes}
          renderItem={(item) => (
            <List.Item
              actions={[
                <Form.Item
                  key={item.key}
                  name={item.key}
                  valuePropName="checked"
                  initialValue={true}
                  style={{ margin: 0 }}
                >
                  <Switch />
                </Form.Item>,
              ]}
            >
              <List.Item.Meta title={item.title} description={item.description} />
            </List.Item>
          )}
        />

        <Divider />

        <h4>Delivery Methods</h4>
        <Form.Item
          name="email_notifications"
          label="Email Notifications"
          valuePropName="checked"
          initialValue={true}
        >
          <Switch />
        </Form.Item>

        <Form.Item
          name="browser_notifications"
          label="Browser Notifications"
          valuePropName="checked"
          initialValue={false}
        >
          <Switch />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save Preferences
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
