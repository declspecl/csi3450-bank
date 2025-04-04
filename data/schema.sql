CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    routing_number CHAR(9) NOT NULL UNIQUE,
    location TEXT NOT NULL,
    phone_number CHAR(14) NOT NULL
);

CREATE TABLE IF NOT EXISTS people (
    person_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birthday DATE NOT NULL,
    email TEXT NOT NULL,
    phone_number CHAR(14) NOT NULL,
    address TEXT NOT NULL,
    ssn CHAR(11) NOT NULL,
    credit_score INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    account_number VARCHAR(17) NOT NULL UNIQUE,
    routing_number CHAR(9) NOT NULL UNIQUE,
    account_type TEXT NOT NULL,
    balance NUMERIC NOT NULL DEFAULT 0,
    status TEXT NOT NULL,
    fk_person_id INTEGER NOT NULL REFERENCES people(person_id),
    fk_bank_id INTEGER NOT NULL REFERENCES banks(bank_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    amount NUMERIC NOT NULL,
    transaction_date DATE NOT NULL,
    status TEXT NOT NULL,
    fk_sender_id INTEGER NOT NULL REFERENCES accounts(account_id),
    fk_recipient_id INTEGER NOT NULL REFERENCES accounts(account_id),
    CONSTRAINT sender_not_recipient CHECK (fk_sender_id <> fk_recipient_id)
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    open_date DATE NOT NULL,
    term_length INTEGER NOT NULL,
    amount NUMERIC NOT NULL,
    status TEXT NOT NULL,
    interest_rate NUMERIC NOT NULL,
    fk_person_id INTEGER NOT NULL REFERENCES people(person_id),
    fk_bank_id INTEGER NOT NULL REFERENCES banks(bank_id)
);

--allows auto incrementing of the primary key in people table to start from the max id in the table
SELECT setval('people_person_id_seq', (SELECT MAX(person_id) FROM people));