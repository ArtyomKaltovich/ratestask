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

create extension ltree;

CREATE TABLE destinations (
  id SERIAL,
  name VARCHAR(50),
  slug VARCHAR(50),
  path ltree,
  is_port BOOLEAN,
  PRIMARY KEY (id)
);

COPY destinations(name, slug, path, is_port)
FROM '/destinations.csv'
DELIMITER ','
CSV HEADER;

CREATE INDEX path_gist_idx ON destinations USING GIST (path);

CREATE TABLE prices (
    orig_code text NOT NULL,
    dest_code text NOT NULL,
    day date NOT NULL,
    price integer NOT NULL
);

COPY destinations(orig_code, dest_code, day, price)
FROM '/destinations.csv'
DELIMITER ','
CSV HEADER;

CREATE INDEX prices_code_idx ON prices USING hash (orig_code, dest_code);
