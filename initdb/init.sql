CREATE TABLE IF NOT EXISTS user_credentials (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_balance (
    user_id INTEGER PRIMARY KEY REFERENCES user_credentials(id),
    balance DECIMAL(10, 2) DEFAULT 0.0 NOT NULL
);

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS celery_tasks (
    id SERIAL PRIMARY KEY,
    celery_task VARCHAR(100) NOT NULL,
    model_id INTEGER REFERENCES models(id) NOT NULL,
    input_data JSONB NOT NULL,
    prediction BOOLEAN,
    task_result VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_tasks (
    user_id INTEGER REFERENCES user_credentials(id) NOT NULL,
    task_id INTEGER REFERENCES celery_tasks(id) NOT NULL,
    PRIMARY KEY (user_id, task_id)
);

INSERT INTO models (name, cost) VALUES
    ('Linear Regression', 5.0),
    ('Random Forest', 15.0),
    ('Neural Network', 30.0);