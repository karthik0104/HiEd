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
    locale_id INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE application (
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(256),
    user_id INTEGER,
    university_id INTEGER,
    course_id INTEGER,
    year VARCHAR(10),
    admit_term VARCHAR(256),
    area_of_specialization VARCHAR(512),
    gre_score VARCHAR(5),
    toefl_ielts_score VARCHAR(5),
    created_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (university_id) REFERENCES university(id),
    FOREIGN KEY (course_id) REFERENCES course(id)
);

CREATE TABLE course (
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(256),
    university_id INTEGER,
    website VARCHAR(256),
    deadline VARCHAR(512),
    address VARCHAR(256),
    contact_number VARCHAR(256),
    email VARCHAR(256),
    acceptance_rate FLOAT,
    acceptance_rate_source VARCHAR(256),
    quant_cutoff INTEGER,
    verbal_cutoff INTEGER,
    toefl_cutoff INTEGER,
    cutoff_source VARCHAR(256),
    ranking INTEGER,
    ranking_source VARCHAR(256),
    batch_size INTEGER,
    batch_size_source VARCHAR(256),
    annual_fees VARCHAR(256),
    annual_fees_source VARCHAR(256),
    is_internship_mandatory TINYINT(1),
    PRIMARY KEY (id),
    FOREIGN KEY (university_id) REFERENCES university(id)
);

CREATE TABLE locale (
    id INTEGER AUTO_INCREMENT,
    language VARCHAR(64),
    PRIMARY KEY (id)
);

CREATE TABLE locale_bundle (
    id INTEGER AUTO_INCREMENT,
    screen_name VARCHAR(256),
    field_name VARCHAR(256),
    locale_id INTEGER,
    value VARCHAR(512),
    PRIMARY KEY (id),
    FOREIGN KEY (locale_id) REFERENCES locale(id)
);

CREATE TABLE plan_stage_masterdata (
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(256),
    description VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE plan (
    application_id INTEGER,
    plan_stage_id INTEGER,
    start_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO locale(language) VALUES ('EN');