-- copied from original file
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;
-- end of copy

CREATE TABLE destinations (
  id SERIAL,
  name VARCHAR(50),
  slug VARCHAR(50),
  path VARCHAR(250),
  PRIMARY KEY (id)
);

COPY destinations(name, slug, path)
FROM '/destinations.csv'
DELIMITER ','
CSV HEADER;

create extension ltree;
