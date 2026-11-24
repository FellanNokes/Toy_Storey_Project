USE ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS toy_wh
    WITH 
        WAREHOUSE_SIZE = 'X-Small'
        AUTO_SUSPEND = 300 
        AUTO_RESUME = TRUE
        INITIALLY_SUSPENDED = TRUE
        COMMENT = 'Warehouse for toystore project';