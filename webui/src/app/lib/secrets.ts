import { Secret } from 'app/types'
import { supabase } from './supabase'

export async function getSecrets(): Promise<Secret[]> {
  const { data, error } = await supabase
    .from('secrets')
    .select('*')
    .order('name')

  if (error) {
    console.error('Error fetching secrets:', error)
    return []
  }

  return data
}