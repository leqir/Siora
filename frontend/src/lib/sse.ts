// lib/sse.ts
import { useEffect, useRef, useState } from 'react';

export type StreamState = {
  status: 'idle' | 'connecting' | 'streaming' | 'done' | 'error';
  text: string;
  thinking: boolean;
  error?: string;
};

export function useSSE(url: string | null) {
  const [state, setState] = useState<StreamState>({
    status: 'idle',
    text: '',
    thinking: false,
  });
  const sourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!url) return;

    setState({ status: 'connecting', text: '', thinking: true });

    // Include cookies with cross-site SSE
    const es = new EventSource(url, { withCredentials: true });
    sourceRef.current = es;

    es.addEventListener('status', () => {
      setState((s) => ({ ...s, thinking: true }));
    });

    es.addEventListener('message', (evt) => {
      setState((s) => ({
        ...s,
        status: 'streaming',
        thinking: false,
        text: s.text + (evt as MessageEvent).data,
      }));
    });

    es.addEventListener('done', () => {
      setState((s) => ({ ...s, status: 'done' }));
      es.close();
    });

    es.onerror = () => {
      setState((s) => ({ ...s, status: 'error', error: 'Stream error', thinking: false }));
      es.close();
    };

    return () => {
      es.close();
    };
  }, [url]);

  return state;
}
