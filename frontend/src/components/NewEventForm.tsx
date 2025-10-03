/* eslint-disable @typescript-eslint/no-floating-promises, 
                  @typescript-eslint/no-explicit-any, 
                  @typescript-eslint/no-unsafe-member-access, 
                  @typescript-eslint/no-unsafe-argument */

                  // components/NewEventForm.tsx
'use client';

import { createEvent } from '../lib/api';
import { useState } from 'react';

type CalEvent = { id: string; summary?: string; start_iso?: string; end_iso?: string; status?: string };

export default function NewEventForm({ onAdd }: { onAdd: (e: CalEvent) => void }) {
  const [summary, setSummary] = useState('');
  const [start, setStart] = useState(''); // ISO like 2025-10-01T15:00:00+10:00
  const [end, setEnd] = useState('');
  const [posting, setPosting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!summary || !start || !end) {
      setError('Please fill all fields.');
      return;
    }
    setPosting(true);

    // optimistic placeholder
    const temp: CalEvent = {
      id: `temp-${Date.now()}`,
      summary,
      start_iso: start,
      end_iso: end,
      status: 'tentative',
    };
    onAdd(temp);

    try {
      const res = await createEvent({ summary, start_iso: start, end_iso: end });
      onAdd({ ...res.event }); // parent replaces temp (same id strategy is simple demo)
      setSummary('');
      setStart('');
      setEnd('');
    } catch (err: any) {
      setError(err?.message ?? 'Failed to create event');
    } finally {
      setPosting(false);
    }
  };

  return (
    <form onSubmit={submit} className="space-y-3 rounded-xl border p-4">
      <div className="font-medium">Create Event</div>
      <div className="grid gap-2 sm:grid-cols-3">
        <input
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
          placeholder="Summary (e.g., Call with Andy)"
          className="rounded-lg border p-2"
        />
        <input
          value={start}
          onChange={(e) => setStart(e.target.value)}
          placeholder="Start ISO (2025-10-01T15:00:00+10:00)"
          className="rounded-lg border p-2"
        />
        <input
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          placeholder="End ISO (2025-10-01T16:00:00+10:00)"
          className="rounded-lg border p-2"
        />
      </div>
      <div className="flex items-center gap-3">
        <button
          disabled={posting}
          className="rounded-xl bg-black px-4 py-2 text-white hover:opacity-90 disabled:opacity-50"
        >
          {posting ? 'Creating…' : 'Create'}
        </button>
        {error && <span className="text-sm text-red-600">{error}</span>}
      </div>
    </form>
  );
}
