/** @type {import('next').NextConfig} */

// const endPointUrl = "192.168.124.190";
const endPointUrl = "0.0.0.0";

const nextConfig = {
  // experimental: {
  //   serverActions: true,
  // },
  async headers() {
    return [
      {
        // matching all API routes
        source: "/api/:path*",
        headers: [
          { key: "Access-Control-Allow-Credentials", value: "true" },
          { key: "Access-Control-Allow-Origin", value: "*" }, // replace this your actual origin
          {
            key: "Access-Control-Allow-Methods",
            value: "GET,DELETE,PATCH,POST,PUT",
          },
          {
            key: "Access-Control-Allow-Headers",
            value:
              "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version",
          },
        ],
      },
    ];
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "static.wixstatic.com",
        port: "",
        pathname: "/media/**",
      },
      {
        protocol: "http",
        hostname: `${endPointUrl}`,
        port: "8000",
        pathname: "/product/**",
      },
      {
        protocol: "http",
        hostname: `${endPointUrl}`,
        port: "8000",
        pathname: "/profile/**",
      },
    ],
  },
};

module.exports = nextConfig;
