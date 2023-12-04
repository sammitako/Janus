import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(req: NextRequest) {
  // Check if the request is for the API route
  // Rewrite the request URL to your backend server
  const backendUrl = "http://127.0.0.1:3000";
  return NextResponse.rewrite(backendUrl);
}