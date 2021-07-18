DROP DATABASE IF EXISTS hied;
CREATE DATABASE hied;

USE hied;

CREATE TABLE university (
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(256),
    PRIMARY KEY (id)
);

CREATE TABLE user (
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(256),
    public_id VARCHAR(512),
    password VARCHAR(512),
    PRIMARY KEY (id)
);

CREATE TABLE application (
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(256),
    user_id VARCHAR(256),
    PRIMARY KEY (id)
);