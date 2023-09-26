import { NextResponse } from "next/server";
import { ENDPOINT_URL } from "@/app/utils/constants";
import { headers } from "next/headers";

export async function POST(request, { params }) {
  const productId = params?.name;
  const headersList = headers();
  const token = headersList.get("token");
  const payload = await request.formData();

  const data = await fetch(
    `${ENDPOINT_URL}/api/v1/products/upload/image/${productId}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: payload,
    }
  );
  const response = await data.json();
  return new NextResponse(JSON.stringify(response));
}
