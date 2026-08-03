CREATE DATABASE IF NOT EXISTS clubtime;
USE clubtime;

CREATE TABLE IF NOT EXISTS users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    username      VARCHAR(50)  NOT NULL UNIQUE, 
    email         VARCHAR(120) NOT NULL UNIQUE, 
    phone_number  VARCHAR(20),
    dob           DATE, 
    join_date     DATE NOT NULL DEFAULT (CURRENT_DATE),
    password_hash VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS admins (
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
