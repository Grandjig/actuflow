-- =============================================================================
-- ActuFlow Database Initialization
-- =============================================================================
-- This script runs when PostgreSQL container is first created
-- =============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";  -- pgvector for embeddings

-- Create schemas
CREATE SCHEMA IF NOT EXISTS actuflow;

-- Set default search path
ALTER DATABASE actuflow SET search_path TO actuflow, public;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA actuflow TO actuflow;
GRANT ALL PRIVILEGES ON SCHEMA public TO actuflow;

-- Create function for updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';
