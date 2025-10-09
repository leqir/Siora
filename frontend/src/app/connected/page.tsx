'use client';

import { useEffect } from 'react';
import Link from 'next/link';

export default function CallbackPage() {
  // Optional auto-redirect after 3 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      window.location.href = '/'; // redirect to homepage
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-white p-6">
      <div className="rounded-2xl border p-8 shadow-md max-w-xl text-center">
        <h1 className="text-3xl font-semibold mb-4">You’re connected 🎉</h1>
        <p className="text-gray-600 mb-6">
          Your Google Calendar is now linked. You’ll be redirected shortly, or you can head back manually.
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
