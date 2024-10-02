CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    surname VARCHAR(255),
    name VARCHAR(255),
    middlename VARCHAR(255),
    phone VARCHAR(15),
    message TEXT
);