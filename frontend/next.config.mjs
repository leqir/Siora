/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,   // ✅ disables ESLint errors in builds
  },
  typescript: {
    ignoreBuildErrors: true,    // ✅ disables TS errors in builds
  },
};

export default nextConfig;
