import { useNavigate } from 'react-router-dom';
import { Result, Button } from 'antd';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <Result
      status="404"
      title="404"
      subTitle="Sorry, the page you visited does not exist."
      extra={
        <Button type="primary" onClick={() => navigate('/dashboard')}>
          Back to Dashboard
        </Button>
      }
    />
  );
}
