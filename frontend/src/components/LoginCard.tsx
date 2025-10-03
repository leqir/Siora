// components/LoginCard.tsx
'use client';

import { getAuthLoginUrl } from '../lib/api';

export default function LoginCard() {
  const onConnect = () => {
    window.location.href = getAuthLoginUrl();
  };

  return (
    <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="mb-3 text-xl font-semibold">Connect Google Calendar</h2>
      <p className="mb-5 text-sm text-gray-600">
        Sign in with Google to let the assistant read and create your calendar events.
      </p>
      <button
        onClick={onConnect}
        className="inline-flex items-center justify-center rounded-xl border bg-black px-4 py-2 text-white transition hover:opacity-90"
      >
        <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24"><path fill="currentColor" d="M21.35 11.1h-9.18v2.98h5.62c-.24 1.52-1.69 4.45-5.62 4.45c-3.38 0-6.15-2.79-6.15-6.23c0-3.45 2.77-6.24 6.15-6.24c1.93 0 3.23.82 3.97 1.53l2.71-2.62C17.75 3.19 15.66 2 12.17 2C6.82 2 2.5 6.33 2.5 11.6c0 5.26 4.32 9.6 9.67 9.6c5.58 0 9.26-3.92 9.26-9.46c0-.64-.07-1.1-.08-1.64Z"/></svg>
        Sign in with Google
      </button>
    </div>
  );
}
