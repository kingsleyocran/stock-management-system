import { NextResponse } from "next/server";
import { ENDPOINT_URL } from "@/app/utils/constants";

export async function GET(request, { params }) {
  const name = params?.name;
  const data = await fetch(`${ENDPOINT_URL}/api/v1/products/name/${name}`, {
    method: "GET",
  });
  const response = await data.json();
  return new NextResponse(JSON.stringify(response));
}
