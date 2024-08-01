CREATE DATABASE PrisonerDatabase;

USE PrisonerDatabase;

CREATE TABLE Prisoners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    sentence_length INT,
    education_level INT,
    behavior_score INT,
    release_recommendation BOOLEAN,
    language_code VARCHAR(10)
);
