import { execute_sql } from './supabase-functions'

export async function query(sql: string, params?: any[]) {
  const start = Date.now()
  const data = await execute_sql(sql, params)
  const duration = Date.now() - start
  console.log('executed query', { sql, duration, rows: data?.length })

  return { rows: data }
}