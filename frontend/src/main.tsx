import React from 'react';
import ReactDOM from 'react-dom/client';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import App from './App';
import './styles/global.css';

// Configure dayjs
dayjs.extend(relativeTime);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
