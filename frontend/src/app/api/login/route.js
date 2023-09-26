import { NextResponse } from "next/server";
import { ENDPOINT_URL } from "@/app/utils/constants";

export async function POST(request) {
  const value = await request.json();
  const response = await fetch(`${ENDPOINT_URL}/api/v1/accounts/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(value),
  });
  const credential = await response.json();
  return new NextResponse(JSON.stringify(credential));
}
