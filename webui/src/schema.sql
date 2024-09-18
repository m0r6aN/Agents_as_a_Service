--supabase schema 
-- https://supabase.com/docs/guides/database/schema

-- Create processes table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'processes') THEN
        CREATE TABLE public.processes (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
END $$;

-- Create tasks table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tasks') THEN
        CREATE TABLE public.tasks (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            process_id UUID REFERENCES public.processes(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
END $$;

-- Create tools table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tools') THEN
        CREATE TABLE public.tools (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
END $$;

-- Create agents table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'agents') THEN
        CREATE TABLE public.agents (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
END $$;

-- Create process_tools junction table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'process_tools') THEN
        CREATE TABLE public.process_tools (
            process_id UUID REFERENCES public.processes(id) ON DELETE CASCADE,
            tool_id UUID REFERENCES public.tools(id) ON DELETE CASCADE,
            PRIMARY KEY (process_id, tool_id)
        );
    END IF;
END $$;

-- Create process_agents junction table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'process_agents') THEN
        CREATE TABLE public.process_agents (
            process_id UUID REFERENCES public.processes(id) ON DELETE CASCADE,
            agent_id UUID REFERENCES public.agents(id) ON DELETE CASCADE,
            PRIMARY KEY (process_id, agent_id)
        );
    END IF;
END $$;

-- Create workflow_steps table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'workflow_steps') THEN
        CREATE TABLE public.workflow_steps (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            process_id UUID REFERENCES public.processes(id) ON DELETE CASCADE,
            task_id UUID REFERENCES public.tasks(id) ON DELETE CASCADE,
            agent_id UUID REFERENCES public.agents(id) ON DELETE CASCADE,
            depends_on_tasks TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
END $$;

-- Create workflow_tools junction table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'workflow_tools') THEN
        CREATE TABLE public.workflow_tools (
            workflow_step_id UUID REFERENCES public.workflow_steps(id) ON DELETE CASCADE,
            tool_id UUID REFERENCES public.tools(id) ON DELETE CASCADE,
            PRIMARY KEY (workflow_step_id, tool_id)
        );
    END IF;
END $$;