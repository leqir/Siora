'use client';

export const dynamic = 'force-dynamic';
export const fetchCache = 'force-no-store';

import { Suspense, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Cookies from 'js-cookie';
import Link from 'next/link';

// Inner component (where useSearchParams is used)
function CallbackInner() {
  const params = useSearchParams();

  useEffect(() => {
    const session = params.get('session');
    if (session) {
      Cookies.set('session', session, { expires: 30 });
    }

    const timer = setTimeout(() => {
      window.location.href = '/';
    }, 3000);

    return () => clearTimeout(timer);
  }, [params]);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6">
      <div className="rounded-2xl border p-8 shadow-lg max-w-xl text-center bg-white">
        <h1 className="text-3xl font-semibold mb-3">You’re connected 🎉</h1>
        <p className="text-gray-600 mb-6">
          Your Google Calendar is now linked.<br />
          Redirecting you to your dashboard...
        </p>
        <Link href="/" className="bg-black text-white px-6 py-2 rounded-xl">
          Go now
        </Link>
      </div>
    </main>
  );
}

// Parent component wrapped in Suspense
export default function CallbackPage() {
  return (
    <Suspense fallback={<div>Loading connection status...</div>}>
      <CallbackInner />
    </Suspense>
  );
}
