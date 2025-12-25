-- SQL Schema for Supabase Data Tier
-- Run this in your Supabase SQL Editor

-- 1. Create the tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high'))
);

-- 2. Enable Row Level Security (RLS) - Optional but recommended
-- ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- 3. Create a policy to allow all actions (for demo purposes)
-- CREATE POLICY "Allow all actions for now" ON tasks FOR ALL USING (true);
