import { NextResponse } from 'next/server';

export async function GET() {
  // Return a simple JSON response indicating the service is healthy
  return NextResponse.json({ status: 'ok', message: 'Service is healthy' });
}

