import { Tabs, Card } from 'antd';
import { UserOutlined, BellOutlined, RobotOutlined, LockOutlined } from '@ant-design/icons';

import PageHeader from '@/components/common/PageHeader';
import ProfileSettings from './ProfileSettings';
import NotificationSettings from './NotificationSettings';
import AISettings from './AISettings';

export default function Settings() {
  return (
    <>
      <PageHeader
        title="Settings"
        subtitle="Manage your account and preferences"
        breadcrumbs={[{ title: 'Settings' }]}
      />

      <Card>
        <Tabs
          tabPosition="left"
          items={[
            {
              key: 'profile',
              label: (
                <span>
                  <UserOutlined /> Profile
                </span>
              ),
              children: <ProfileSettings />,
            },
            {
              key: 'notifications',
              label: (
                <span>
                  <BellOutlined /> Notifications
                </span>
              ),
              children: <NotificationSettings />,
            },
            {
              key: 'ai',
              label: (
                <span>
                  <RobotOutlined /> AI Preferences
                </span>
              ),
              children: <AISettings />,
            },
          ]}
        />
      </Card>
    </>
  );
}
