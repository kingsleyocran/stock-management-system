import { NextResponse } from "next/server";
import { ENDPOINT_URL } from "@/app/utils/constants";

export async function POST(request) {
  const value = await request.json();

  const data = await fetch(`${ENDPOINT_URL}/api/v1/orders/make`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: `Bearer ${value.token}`,
    },
    body: JSON.stringify(value.payload),
  });
  const response = await data.json();
  return new NextResponse(JSON.stringify(response));
}
