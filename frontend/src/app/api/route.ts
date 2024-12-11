import { NextResponse } from 'next/server'

// Health check endpoint
export async function GET() {
  try {
    return NextResponse.json(
      { status: 'API is healthy' },
      { status: 200 }
    )
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    )
  }
}