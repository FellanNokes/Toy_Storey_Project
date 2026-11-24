USE ROLE SYSADMIN;

-- Create the Ice Cream database
CREATE DATABASE IF NOT EXISTS toy_storey;

CREATE SCHEMA IF NOT EXISTS toy_storey.staging;
CREATE SCHEMA IF NOT EXISTS toy_storey.warehouse;
CREATE SCHEMA IF NOT EXISTS toy_storey.marts;