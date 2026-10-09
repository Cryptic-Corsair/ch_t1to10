import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // standalone output powers the sandbox/FC deployment (custom server +
  // start.sh). Vercel builds and serves with its own pipeline, where
  // standalone is unnecessary — so disable it there.
  output: process.env.VERCEL ? undefined : "standalone",
  devIndicators: false,
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
};

export default nextConfig;
