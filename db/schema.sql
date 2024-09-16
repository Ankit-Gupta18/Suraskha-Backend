-- Create user_auth_db table
CREATE TABLE user_auth_db (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    adhaar_number VARCHAR(12) NOT NULL UNIQUE,
    state VARCHAR(100),
    age_group VARCHAR(20),
    gender VARCHAR(10),
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    avatar BYTEA,  -- Storing the image as binary data (BYTEA)
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Create police_auth_db table
CREATE TABLE police_auth_db (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    police_id VARCHAR(50) NOT NULL UNIQUE,
    police_station_address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    id_card BYTEA,  -- Storing the ID card image as binary data (BYTEA)
    avatar BYTEA,   -- Storing the avatar image as binary data (BYTEA)
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Triggers for updating 'updated_at' on row modification for both tables
CREATE OR REPLACE FUNCTION update_timestamp() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for user_auth_db
CREATE TRIGGER update_user_auth_timestamp
BEFORE UPDATE ON user_auth_db
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Trigger for police_auth_db
CREATE TRIGGER update_police_auth_timestamp
BEFORE UPDATE ON police_auth_db
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
