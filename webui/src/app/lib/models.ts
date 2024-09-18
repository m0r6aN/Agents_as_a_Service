
import { Model } from 'app/types'
import { supabase } from './supabase'

export async function getTools(): Promise<Model[]> {
  const { data, error } = await supabase
    .from('models')
    .select('*')
    .order('name')

  if (error) {
    console.error('Error fetching tools:', error)
    return []
  }

  return data
}