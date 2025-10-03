// lib/api.ts
const BASE = process.env.NEXT_PUBLIC_BACKEND_URL!;

function withCreds(init?: RequestInit): RequestInit {
  return {
    ...init,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
  };
}

export async function getHealth() {
  const r = await fetch(`${BASE}/healthz`, withCreds());
  return r.ok;
}

export async function getEvents(): Promise<
  { events: { id: string; summary?: string; start_iso?: string; end_iso?: string; status?: string }[] }
> {
  const r = await fetch(`${BASE}/calendar/events`, withCreds());
  if (r.status === 401) throw new Error('unauthorized');
  if (!r.ok) throw new Error('failed');
  return r.json();
}

export async function createEvent(body: {
  summary: string;
  start_iso: string;
  end_iso: string;
}) {
  const r = await fetch(`${BASE}/calendar/events`, withCreds({
    method: 'POST',
    body: JSON.stringify(body),
  }));
  if (r.status === 401) throw new Error('unauthorized');
  if (!r.ok) throw new Error('failed');
  return r.json();
}

export function getAuthLoginUrl() {
  return `${BASE}/auth/login`;
}
