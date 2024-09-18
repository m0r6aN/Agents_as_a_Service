import { supabase } from './supabase'

export interface Function {
  id: string
  name: string
  description: string
  language: string
  code: string
}

export async function getFunctions(): Promise<Function[]> {
  const { data, error } = await supabase
    .from('functions')
    .select('*')
    .order('name')

  if (error) {
    console.error('Error fetching functions:', error)
    return []
  }

  return data
}