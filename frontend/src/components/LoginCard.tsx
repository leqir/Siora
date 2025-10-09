'use client';
import React from "react";

export default function LoginCard() {
  const handleGoogleLogin = () => {
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/auth/login`;
  };

  return (
    <div className="p-6 border rounded-2xl shadow-md text-center bg-white">
      <h2 className="text-xl font-semibold mb-3">Connect your Google Calendar</h2>
      <p className="text-gray-600 mb-4">Sign in to sync and manage your events seamlessly.</p>
      <button
        onClick={handleGoogleLogin}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
      >
        Sign in with Google
      </button>
    </div>
  );
}
