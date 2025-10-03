// components/CalendarEvents.tsx
'use client';

import { useEffect, useState } from 'react';
import { getEvents } from '../lib/api';

type CalEvent = { id: string; summary?: string; start_iso?: string; end_iso?: string; status?: string };

export default function CalendarEvents() {
  const [events, setEvents] = useState<CalEvent[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await getEvents();
        setEvents(data.events);
      } catch (e: any) {
        setError(e?.message ?? 'Failed to load');
      }
    })();
  }, []);

  if (error === 'unauthorized') return (
    <div className="rounded-xl border border-amber-300 bg-amber-50 p-4 text-amber-800">
      You’re not connected yet. Click <strong>Sign in with Google</strong> to connect your calendar.
    </div>
  );

  if (!events) return <div className="text-gray-500">Loading your upcoming events…</div>;
  if (!events.length) return <div className="text-gray-500">No upcoming events found.</div>;

  return (
    <ul className="space-y-2">
      {events.map((e) => (
        <li key={e.id} className="rounded-xl border p-3">
          <div className="font-medium">{e.summary ?? '(No title)'}</div>
          <div className="text-sm text-gray-600">
            {e.start_iso} → {e.end_iso}
          </div>
        </li>
      ))}
    </ul>
  );
}
