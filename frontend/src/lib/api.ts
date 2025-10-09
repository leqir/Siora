// lib/api.ts
const BASE = process.env.NEXT_PUBLIC_BACKEND_URL!;

function withCreds(init?: RequestInit): RequestInit {
  return {
    ...init,
    credentials: 'include', // ✅ ensures cookies are sent
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
  };
}

// Health check
export async function getHealth() {
  const r = await fetch(`${BASE}/healthz`, withCreds());
  return r.ok;
}

// Get events (fixed URL + credentials)
export async function getEvents() {
  const res = await fetch(`${BASE}/events`, withCreds());
  
  if (res.status === 401) throw new Error("unauthorized");
  if (!res.ok) throw new Error(`error ${res.status}`);
  
  return await res.json();
}

// Create new calendar event
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

// Get Google Auth URL
export function getAuthLoginUrl() {
  return `${BASE}/auth/login`;
}
