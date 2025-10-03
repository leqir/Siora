/* eslint-disable @typescript-eslint/no-floating-promises, 
                  @typescript-eslint/no-explicit-any, 
                  @typescript-eslint/no-unsafe-member-access, 
                  @typescript-eslint/no-unsafe-argument */

                  // app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import LoginCard from '../components/LoginCard';
import Chat from '../components/Chat';
import CalendarEvents from '../components/CalendarEvents';
import NewEventForm from '../components/NewEventForm';
import { getEvents } from '../lib/api';

type CalEvent = { id: string; summary?: string; start_iso?: string; end_iso?: string; status?: string };

export default function HomePage() {
  const [connected, setConnected] = useState<boolean | null>(null);
  const [events, setEvents] = useState<CalEvent[]>([]);

  useEffect(() => {
    (async () => {
      try {
        const { events } = await getEvents();
        setConnected(true);
        setEvents(events);
      } catch (e: any) {
        if (e?.message === 'unauthorized') {
          setConnected(false);
        } else {
          setConnected(true); // backend could be up but empty or error; still show UI
        }
      }
    })();
  }, []);

  const handleAdd = (ev: CalEvent) => {
    // simple optimistic strategy:
    setEvents((prev) => {
      // if we receive a real ID for an existing temp-id event, replace by summary match
      const existingIdx = prev.findIndex((p) => p.id === ev.id || p.summary === ev.summary);
      if (existingIdx >= 0) {
        const copy = [...prev];
        copy[existingIdx] = ev;
        return copy;
      }
      return [ev, ...prev];
    });
  };

  return (
    <main className="mx-auto max-w-5xl p-6">
      <header className="mb-6">
        <h1 className="text-3xl font-semibold">{process.env.NEXT_PUBLIC_APP_NAME}</h1>
        <p className="text-gray-600">Chat to your calendar. Create, find, and confirm events in seconds.</p>
      </header>

      {connected === false && (
        <div className="flex justify-center">
          <LoginCard />
        </div>
      )}

      {connected && (
        <div className="grid gap-6 md:grid-cols-3">
          <div className="md:col-span-2 space-y-6">
            <Chat />
            <NewEventForm onAdd={handleAdd} />
            <div className="rounded-2xl border p-4">
              <div className="mb-2 font-medium">Upcoming</div>
              <ul className="space-y-2">
                {events.length === 0 && <li className="text-gray-500">No events yet.</li>}
                {events.map((e) => (
                  <li key={e.id} className="rounded-xl border p-3">
                    <div className="font-medium">{e.summary ?? '(No title)'}</div>
                    <div className="text-sm text-gray-600">{e.start_iso} → {e.end_iso}</div>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <aside className="space-y-4">
            <div className="rounded-2xl border p-4">
              <div className="mb-2 font-medium">Live Calendar</div>
              <CalendarEvents />
            </div>
          </aside>
        </div>
      )}

      {connected === null && <div className="text-gray-500">Checking connection…</div>}
    </main>
  );
}
