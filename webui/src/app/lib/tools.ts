
import { Tool } from '../types'
import { supabase } from './supabase'

export async function getTools(): Promise<Tool[]> {
  const { data, error } = await supabase
    .from('tools')
    .select('*')
    .order('name')

  if (error) {
    console.error('Error fetching tools:', error)
    return []
  }

  return data
}