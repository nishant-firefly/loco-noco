-- Create the user table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert sample data into user table
INSERT INTO "user" (id, username, email) VALUES (1, 'John Doe', 'john.doe@example.com');
INSERT INTO "user" (id, username, email) VALUES (2, 'Jane Smith', 'jane.smith@example.com');

-- Create the product table
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price INT,
    is_active BOOLEAN DEFAULT TRUE,
    category_id INT REFERENCES category(id)
);

-- Insert sample data into product table
INSERT INTO product (id, name, price, is_active, category_id) VALUES (1, 'Gaming Laptop', 1500, TRUE, 1);
INSERT INTO product (id, name, price, is_active, category_id) VALUES (2, 'Smartphone', 800, TRUE, 2);

-- Create the product_category table
CREATE TABLE IF NOT EXISTS product_category (
    product_id INT REFERENCES product(id),
    category_id INT REFERENCES category(id),
    PRIMARY KEY (product_id, category_id)
);

-- Insert sample data into product_category table
INSERT INTO product_category (product_id, category_id) VALUES (1, 1);
INSERT INTO product_category (product_id, category_id) VALUES (2, 2);
