import { NextResponse } from 'next/server'
import { query } from '@/lib/db'

export async function GET() {
  try {
    const result = await query('SELECT name FROM model_types ORDER BY name')
    return NextResponse.json(result.rows.map(row => row.name))
  } catch (error) {
    console.error('Database query error:', error)
    return NextResponse.json({ message: 'Error fetching model types' }, { status: 500 })
  }
}