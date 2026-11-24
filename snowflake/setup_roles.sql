USE ROLE USERADMIN;

-- Create Roles
CREATE ROLE IF NOT EXISTS toy_dlt_role;
CREATE ROLE IF NOT EXISTS toy_dbt_role;
CREATE ROLE IF NOT EXISTS toy_reporter_role;
CREATE ROLE IF NOT EXISTS engineer_role;


USE ROLE securityadmin;

-- DLT role
GRANT USAGE ON WAREHOUSE toy_wh TO ROLE toy_dlt_role;
GRANT USAGE ON DATABASE toy_storey TO ROLE toy_dlt_role;
GRANT USAGE, CREATE TABLE, CREATE STAGE, CREATE FILE FORMAT ON SCHEMA toy_storey.staging TO ROLE toy_dlt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA toy_storey.staging TO ROLE toy_dlt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA toy_storey.staging TO ROLE toy_dlt_role;

-- DBT role
GRANT ROLE toy_dlt_role TO ROLE toy_dbt_role;

GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA toy_storey.warehouse TO ROLE toy_dbt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA toy_storey.warehouse TO ROLE toy_dbt_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA toy_storey.warehouse TO ROLE toy_dbt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA toy_storey.warehouse TO ROLE toy_dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA toy_storey.warehouse TO ROLE toy_dbt_role;

GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA toy_storey.marts TO ROLE toy_dbt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA toy_storey.marts TO ROLE toy_dbt_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA toy_storey.marts TO ROLE toy_dbt_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA toy_storey.marts TO ROLE toy_dbt_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA toy_storey.marts TO ROLE toy_dbt_role;

-- Reporter role
GRANT USAGE ON WAREHOUSE toy_wh TO ROLE toy_reporter_role;
GRANT USAGE ON DATABASE toy_storey TO ROLE toy_reporter_role;
GRANT USAGE ON SCHEMA toy_storey.marts TO ROLE toy_reporter_role;
GRANT SELECT ON ALL TABLES IN SCHEMA toy_storey.marts TO ROLE toy_reporter_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA toy_storey.marts TO ROLE toy_reporter_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA toy_storey.marts TO ROLE toy_reporter_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA toy_storey.marts TO ROLE toy_reporter_role;

-- Data Engineer role
GRANT ROLE toy_dlt_role TO ROLE engineer_role;
GRANT ROLE toy_dbt_role TO ROLE engineer_role;
GRANT ROLE toy_reporter_role TO ROLE engineer_role;
GRANT ROLE engineer_role TO ROLE SYSADMIN;
