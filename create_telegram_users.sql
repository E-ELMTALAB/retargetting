CREATE TABLE IF NOT EXISTS telegram_users (
    chat_id BIGINT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT
);
