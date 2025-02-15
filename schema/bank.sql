CREATE TABLE IF NOT EXISTS bank (
    bank_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    -- ...
);

