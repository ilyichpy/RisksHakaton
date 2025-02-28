CREATE TABLE IF NOT EXISTS user_info (
    id SERIAL PRIMARY KEY,
    fio VARCHAR(100) NOT NULL,
    birth_date VARCHAR(100) NOT NULL,
    hometown VARCHAR(100) NOT NULL,
    dul_client VARCHAR(200) NOT NULL

);

-- insert с персональными данными.