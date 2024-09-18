import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY

if (!supabaseUrl || !supabaseKey) {
  throw new Error('Missing Supabase environment variables')
}

const supabase = createClient(supabaseUrl, supabaseKey)

export async function generateResponse(prompt: string): Promise<string> {
  try {
    const { data, error } = await supabase.functions.invoke('ai-service', {
      body: JSON.stringify({ prompt }),
    })

    if (error) throw error

    return data.response
  } catch (error) {
    console.error('Error generating AI response:', error)
    return 'Sorry, I encountered an error while processing your request.'
  }
}