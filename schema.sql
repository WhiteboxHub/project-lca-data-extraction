CREATE SCHEMA IF NOT EXISTS whitebox_learning;

CREATE TABLE IF NOT EXISTS whitebox_learning.company_hr_contacts (
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    company_name VARCHAR(255),
    location VARCHAR(500),
    job_title VARCHAR(255),
    extraction_date TIMESTAMP
);
