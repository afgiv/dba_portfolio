/* Make sure to be connected as the dba role */


-- Create the schemas for roles for their usage
CREATE SCHEMA app AUTHORIZATION app_user;
CREATE SCHEMA etl;
CREATE SCHEMA analysis;
CREATE SCHEMA qa;
