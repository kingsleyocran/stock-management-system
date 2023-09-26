import { NextResponse } from "next/server";
import { ENDPOINT_URL } from "@/app/utils/constants";

export async function GET(request) {
  const size = request.nextUrl.searchParams.get("size");
  const page = request.nextUrl.searchParams.get("page");
  const data = await fetch(
    `${ENDPOINT_URL}/api/v1/products/all?page=${page}&size=${size}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-cache",
    }
  );
  const response = await data.json();
  return new NextResponse(JSON.stringify(response));
}

export async function POST(request) {
  const payload = await request.json();
  const value = JSON.stringify(payload?.payload);
  const data = await fetch(`${ENDPOINT_URL}/api/v1/products/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${payload?.token}`,
    },
    body: value,
  });
  const response = await data.json();
  return new NextResponse(JSON.stringify(response));
}
