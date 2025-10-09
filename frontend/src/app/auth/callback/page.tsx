'use client';

import { useEffect } from 'react';
import Link from 'next/link';

export default function CallbackPage() {
  useEffect(() => {
    const timer = setTimeout(() => {
      window.location.href = '/';
    }, 4000); // redirect after 4 seconds
    return () => clearTimeout(timer);
  }, []);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6">
      <div className="rounded-2xl border p-8 shadow-lg max-w-xl text-center bg-white">
        <h1 className="text-3xl font-semibold mb-3">You’re connected 🎉</h1>
        <p className="text-gray-600 mb-6">
          Your Google Calendar is now linked.
          <br /> You’ll be redirected shortly, or you can return manually.
        </p>
        <Link
          href="/"
          className="inline-block bg-black text-white px-6 py-2 rounded-xl hover:bg-gray-800 transition"
        >
          Return to Homepage
        </Link>
      </div>
    </main>
  );
}
