CREATE TABLE IF NOT EXISTS user_credentials (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_balance (
    user_id INTEGER PRIMARY KEY REFERENCES user_credentials(id),
    balance DECIMAL(10, 2) DEFAULT 0.0 NOT NULL
);