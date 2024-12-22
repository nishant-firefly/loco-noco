-- Create table for products
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INT NOT NULL
);

-- Insert initial data into product table
INSERT INTO product (id, name, price, quantity) VALUES
(2, 'Phone', 800, 15),
(3, 'Tablet', 450, 25),
(4, 'Smartwatch', 250, 30),
(5, 'Headphones', 150, 50);

-- Create table for customers
CREATE TABLE IF NOT EXISTS customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL
);

-- Insert initial data into customer table
INSERT INTO customer (id, first_name, last_name, email, phone) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '1234567890'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '9876543210'),
(3, 'Michael', 'Johnson', 'michael.johnson@example.com', '5555555555');

-- Create table for orders
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customer(id),
    product_id INT REFERENCES product(id),
    quantity INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial data into orders table
INSERT INTO orders (customer_id, product_id, quantity) VALUES
(1, 2, 1), -- John Doe ordered 1 Phone
(2, 3, 2), -- Jane Smith ordered 2 Tablets
(3, 4, 3); -- Michael Johnson ordered 3 Smartwatches

-- Create table for reviews
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(id),
    customer_id INT REFERENCES customer(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT
);

-- Insert initial data into reviews table
INSERT INTO reviews (product_id, customer_id, rating, review_text) VALUES
(2, 1, 5, 'Excellent phone with great features!'),
(3, 2, 4, 'Nice tablet but the battery could be better.'),
(4, 3, 3, 'Decent smartwatch, but the screen is small.');
(5, 4, 4, 'Good sound quality but a bit tight on the ears.'),
(6, 5, 5, 'Amazing laptop, fast and sleek!');
(8, 6, 4, 'Nice monitor, but could have better color accuracy.'),
(9, 7, 5, 'Perfect mouse for gaming and productivity!');

-- Create table for promotions
CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(id),
    discount_percentage NUMERIC(5, 2),
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP
);

-- Insert initial data into promotions table
INSERT INTO promotions (product_id, discount_percentage, start_date, end_date) VALUES
(2, 10.00, '2024-12-01', '2024-12-31'), -- 10% off on Phone
(3, 15.00, '2024-12-01', '2024-12-15'), -- 15% off on Tablet
(4, 20.00, '2024-12-10', '2024-12-25'); -- 20% off on Smartwatch

-- Create table for stock updates
CREATE TABLE IF NOT EXISTS stock_updates (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(id),
    change_quantity INT NOT NULL,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(255)
);

-- Insert initial data into stock_updates table
INSERT INTO stock_updates (product_id, change_quantity, reason) VALUES
(2, -5, 'Sold in orders'),
(3, -3, 'Sold in orders'),
(4, -2, 'Sold in orders'),
(5, -1, 'Sold in orders'),
(6, -1, 'Sold in orders'),
(7, -2, 'Promotional giveaway');





-- Create table for users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Insert initial data into users table
INSERT INTO users (id, name, email) VALUES
(1, 'Alice', 'alice@example.com'),
(2, 'Bob', 'bob@example.com');








-- -- Update data for product (operation: update)
-- UPDATE product
-- SET name = 'Gaming Laptop', price = 1500, quantity = 5
-- WHERE id = 1;

-- -- Select updated product data
-- SELECT * FROM product WHERE id = 1;

-- -- Delete product (operation: delete)
-- DELETE FROM product WHERE id = 1;

-- -- Select remaining product data (after delete operation)
-- SELECT * FROM product WHERE id = 1;

-- -- Read all products (operation: read)
-- SELECT * FROM product;

-- -- Read all orders (operation: read)
-- SELECT * FROM orders;

-- -- Read all customers (operation: read)
-- SELECT * FROM customer;











