import { useState, useEffect, useRef, useCallback } from 'react';
import { useAuthStore } from '@/stores/authStore';

interface WebSocketOptions {
  enabled?: boolean;
  reconnect?: boolean;
  reconnectAttempts?: number;
  reconnectInterval?: number;
  onOpen?: (event: Event) => void;
  onClose?: (event: CloseEvent) => void;
  onError?: (event: Event) => void;
  onMessage?: (event: MessageEvent) => void;
}

interface WebSocketReturn {
  lastMessage: MessageEvent | null;
  sendMessage: (message: string | object) => void;
  readyState: number;
  connect: () => void;
  disconnect: () => void;
}

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

export function useWebSocket(
  path: string,
  options: WebSocketOptions = {}
): WebSocketReturn {
  const {
    enabled = true,
    reconnect = true,
    reconnectAttempts = 5,
    reconnectInterval = 3000,
    onOpen,
    onClose,
    onError,
    onMessage,
  } = options;

  const token = useAuthStore((state) => state.token);
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CLOSED);
  
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCountRef = useRef(0);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const connect = useCallback(() => {
    if (!enabled || !token) return;

    // Build WebSocket URL with auth token
    const url = `${WS_URL}${path}?token=${token}`;
    
    try {
      wsRef.current = new WebSocket(url);

      wsRef.current.onopen = (event) => {
        setReadyState(WebSocket.OPEN);
        reconnectCountRef.current = 0;
        onOpen?.(event);
      };

      wsRef.current.onclose = (event) => {
        setReadyState(WebSocket.CLOSED);
        onClose?.(event);

        // Attempt reconnection
        if (reconnect && reconnectCountRef.current < reconnectAttempts) {
          reconnectCountRef.current++;
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };

      wsRef.current.onerror = (event) => {
        onError?.(event);
      };

      wsRef.current.onmessage = (event) => {
        setLastMessage(event);
        onMessage?.(event);
      };
    } catch (error) {
      console.error('WebSocket connection error:', error);
    }
  }, [enabled, token, path, reconnect, reconnectAttempts, reconnectInterval, onOpen, onClose, onError, onMessage]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((message: string | object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const data = typeof message === 'string' ? message : JSON.stringify(message);
      wsRef.current.send(data);
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  // Connect on mount
  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    lastMessage,
    sendMessage,
    readyState,
    connect,
    disconnect,
  };
}

export default useWebSocket;
