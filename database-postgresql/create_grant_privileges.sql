/* 
Specify grant privileges for each schema.
The alter default privileges will automatically grant the role to have the
privileges to any tables created within their schema after this command
*/



-- Admin will have full access to all schema
GRANT ALL ON SCHEMA app TO admin;
GRANT ALL ON SCHEMA etl TO admin;
GRANT ALL ON SCHEMA analysis TO admin;
GRANT ALL ON SCHEMA qa TO admin;

-- DBA gets creation and modification rights
GRANT USAGE, CREATE ON SCHEMA app TO dba;
GRANT USAGE, CREATE ON SCHEMA etl TO dba;
GRANT USAGE, CREATE ON SCHEMA analysis TO dba;
GRANT USAGE, CREATE ON SCHEMA qa TO dba;

-- App user access (for Flask app)
GRANT USAGE, CREATE ON SCHEMA app to app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA app
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;


-- Data engineer access (for ETL tasks)
GRANT USAGE, CREATE ON SCHEMA etl TO d_engineer;
GRANT USAGE, CREATE ON SCHEMA analysis TO d_engineer;

-- Data analyst access (read-only for analysis tasks)
GRANT USAGE ON SCHEMA analysis TO d_analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA analysis
GRANT SELECT ON TABLES TO d_analyst;

-- QA Engineer access (for testing DB)
GRANT USAGE ON SCHEMA qa TO qa_engineer;
ALTER DEFAULT PRIVILEGES IN SCHEMA qa
GRANT SELECT, INSERT ON TABLES TO qa_engineer;