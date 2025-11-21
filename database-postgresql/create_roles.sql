-- Admin role (full access)
CREATE ROLE admin WITH LOGIN SUPERUSER PASSWORD 'admin_password';

-- DBA role (for DBA daily management)
CREATE ROLE dba WITH LOGIN PASSWORD 'dba_password';

-- App user (for flask app)
CREATE ROLE app_user WITH LOGIN PASSWORD 'app_password';

-- Data Engineer user (for ETL tasks)
CREATE ROLE d_engineer WITH LOGIN PASSWORD 'de_password';

-- Data Analyst user (for analysis tasks)
CREATE ROLE d_analyst WITH LOGIN PASSWORD 'da_password';

-- QA Engineer (for QA tasks)
CREATE ROLE qa_engineer WITH LOGIN PASSWORD 'qa_password';