import { NextResponse } from "next/server";
import { ENDPOINT_URL } from "@/app/utils/constants";

export async function POST(request) {
  const value = await request.json();
  const response = await fetch(`${ENDPOINT_URL}/api/v1/accounts/logout`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${value?.token}`,
    },
  });
  const credential = await response.json();
  return new NextResponse(JSON.stringify(credential));
}
