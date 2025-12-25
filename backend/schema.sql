-- Optimized Production-Ready Supabase Schema
-- Run this in your Supabase SQL Editor

-- Enable pgcrypto for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Create tasks table in the public schema
CREATE TABLE IF NOT EXISTS public.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    user_id UUID NOT NULL, -- Ties each task to a specific user
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed')),
    priority TEXT NOT NULL DEFAULT 'medium'
        CHECK (priority IN ('low', 'medium', 'high'))
);

-- 2. Enable Row Level Security (RLS)
-- This ensures data isolation between users at the database level
ALTER TABLE public.tasks ENABLE ROW LEVEL SECURITY;

-- 3. RLS Policies (Auth-Link)
-- Note: These policies assume you are using Supabase Auth.
-- The backend (FastAPI) should ideally pass the User's JWT or use a Service Role.

CREATE POLICY "Users can read own tasks"
ON public.tasks
FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own tasks"
ON public.tasks
FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own tasks"
ON public.tasks
FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own tasks"
ON public.tasks
FOR DELETE
USING (auth.uid() = user_id);

-- 4. Development Index
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON public.tasks(user_id);
