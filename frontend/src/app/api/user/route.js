import { NextResponse } from "next/server";
import { ENDPOINT_URL } from "@/app/utils/constants";

export async function POST(request) {
  const value = await request.json();

  const data = await fetch(`${ENDPOINT_URL}/api/v1/accounts/details`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${value?.token}`,
    },
    cache: "default",
  });
  const response = await data.json();
  return new NextResponse(JSON.stringify(response));
}
