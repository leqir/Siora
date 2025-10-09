// lib/api.ts
const BASE = process.env.NEXT_PUBLIC_BACKEND_URL!;
import Cookies from 'js-cookie';

function withCreds(init?: RequestInit): RequestInit {
  
  return {
    ...init,
    credentials: "include",      // <--- this line matters
    headers: {
      "Content-Type": "application/json",
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
  console.log("Fetching events from", `${process.env.NEXT_PUBLIC_BACKEND_URL}/events`);
  const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/events`, {
    credentials: "include",
  });

  console.log("Response status:", res.status);
  const txt = await res.text();
  console.log("Response text:", txt);

  if (res.status === 401) {
    throw new Error("unauthorized");
  }
  if (!res.ok) {
    throw new Error(`error ${res.status}`);
  }
  return JSON.parse(txt);
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
