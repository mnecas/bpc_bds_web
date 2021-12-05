CREATE ROLE bds_user LOGIN ENCRYPTED PASSWORD 'mnecas';
CREATE DATABASE bpc_bds_db OWNER bds_user;
CREATE SCHEMA bpc_bds_db_schema AUTHORIZATION bds_user;
GRANT ALL PRIVILEGES ON DATABASE bpc_bds_db TO bds_user;
