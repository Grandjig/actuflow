-- ActuFlow Database Initialization Script
-- This script is run when PostgreSQL container first starts

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";  -- For AI embeddings

-- Create additional database for Keycloak if needed
CREATE DATABASE keycloak;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE actuflow TO actuflow;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO actuflow;

-- Set timezone
SET timezone = 'UTC';

-- Create schema version tracking table
CREATE TABLE IF NOT EXISTS schema_info (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT INTO schema_info (version, description) 
VALUES ('0.0.0', 'Initial database setup');

-- Output confirmation
DO $$
BEGIN
    RAISE NOTICE 'ActuFlow database initialized successfully';
END
$$;
