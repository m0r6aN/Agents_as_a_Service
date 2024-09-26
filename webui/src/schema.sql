-- Create or alter processes table
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
    ELSE
        -- Alter table to add new columns if needed
        --IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='processes' AND column_name='new_column') THEN
           -- ALTER TABLE public.processes ADD COLUMN new_column TEXT;
        --END IF;
    END IF;
END $$;

-- Create or alter tasks table
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tasks') THEN
        CREATE TABLE public.tasks (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            process_id UUID REFERENCES public.processes(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            dependencies TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    ELSE
        -- Alter table to add new columns if needed
        --IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='tasks' AND column_name='new_column') THEN
           -- ALTER TABLE public.tasks ADD COLUMN new_column TEXT;
        --END IF;
    END IF;
END $$;

-- Create or alter tools table
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'tools') THEN
        CREATE TABLE public.tools (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    ELSE
        -- Alter table to add new columns if needed
       -- IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='tools' AND column_name='new_column') THEN
        --    ALTER TABLE public.tools ADD COLUMN new_column TEXT;
        --END IF;
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
            model_id TEXT,
            inference_url TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        ELSE
         -- Alter table to add new columns if needed
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='tools' AND column_name='new_column') THEN
            ALTER TABLE public.tools DROP COLUMN inference_url;
        END IF;
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

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'models') THEN
        CREATE TABLE public.models (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            type VARCHAR(50) NOT NULL,
            tasks TEXT[],
            system_message TEXT,
            user_message TEXT,
            temperature FLOAT,
            model_source_url TEXT,
            context_window_size INTEGER,
            usage_example TEXT,
            api_key TEXT,
            version VARCHAR(50),
            author VARCHAR(255),
            license TEXT,
            fine_tuning_status VARCHAR(20),
            fine_tuning_dataset TEXT,
            supported_languages TEXT[],
            input_format TEXT[],
            output_format TEXT[],
            max_sequence_length INTEGER,
            batch_size INTEGER,
            quantization VARCHAR(10),
            hardware_requirements TEXT[],
            inference_time FLOAT,
            model_size FLOAT,
            last_updated DATE
        );
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'model_types') THEN
        CREATE TABLE public.model_types (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'agent_tasks') THEN
        CREATE TABLE public.model_tasks (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            model_type_id UUID REFERENCES public.model_types(id),
            name VARCHAR(100) NOT NULL,
            UNIQUE(model_type_id, name)
        );
    END IF;
END $$;
