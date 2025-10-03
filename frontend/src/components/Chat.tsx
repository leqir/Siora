// components/Chat.tsx
'use client';

import { useState } from 'react';
import { useSSE } from '../lib/sse';

const BASE = process.env.NEXT_PUBLIC_BACKEND_URL!;

export default function Chat() {
  const [input, setInput] = useState('');
  const [streamUrl, setStreamUrl] = useState<string | null>(null);
  const state = useSSE(streamUrl);

  const send = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Start a new SSE stream. We POST the body and include cookies.
    // Because EventSource only supports GET, we embed the message as a query param.
    // Backend endpoint is POST-only, so we'll use a small proxy pattern:
    // For simplicity we URL-encode the message into a GET endpoint we prepared on backend (/chat/stream?msg=...).
    // If you kept POST-only, swap to a tiny Next.js API route proxy. For now we assume GET is allowed.
    const url = `${BASE}/chat/stream?message=${encodeURIComponent(input)}`;
    setStreamUrl(url);
    setInput('');
  };

  return (
    <div className="rounded-2xl border p-4">
      <div className="mb-2 font-medium">Chat</div>
      <form onSubmit={send} className="mb-3 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me about your schedule or create an event…"
          className="flex-1 rounded-xl border p-2"
        />
        <button className="rounded-xl bg-black px-4 py-2 text-white hover:opacity-90">
          Send
        </button>
      </form>

      <div className="min-h-[3rem] whitespace-pre-wrap rounded-xl bg-gray-50 p-3 text-sm">
        {state.status === 'idle' && <span className="text-gray-500">No messages yet.</span>}
        {state.status === 'connecting' && <span className="text-gray-500">Connecting…</span>}
        {state.thinking && <span className="animate-pulse text-gray-500">Thinking…</span>}
        {state.text && <span>{state.text}</span>}
        {state.status === 'error' && (
          <span className="text-red-600">Stream error. Please try again.</span>
        )}
      </div>
    </div>
  );
}
