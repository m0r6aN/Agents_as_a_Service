import { supabase } from './supabase'

export interface Config {
  id: string
  name: string
  description: string
  value: any
}

export async function getConfigs(): Promise<Config[]> {
  const { data, error } = await supabase
    .from('configs')
    .select('*')
    .order('name')

  if (error) {
    console.error('Error fetching configs:', error)
    return []
  }

  return data
}