CREATE DATABASE shop;

-- 1 task
CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    is_staff SMALLINT,
    country VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    address TEXT
);
COPY users FROM '/usr/src/users.csv' DELIMITER ',';

CREATE TABLE carts(
    cart_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    subtotal DECIMAL,
    total DECIMAL,
    timestamp TIMESTAMP(2)
);
COPY carts FROM '/usr/src/carts.csv' DELIMITER ',';

CREATE TABLE order_status(
    order_status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(255)
);
COPY order_status FROM '/usr/src/order_statuses.csv' DELIMITER ',';

CREATE TABLE orders(
    order_id SERIAL PRIMARY KEY,
    carts_cart_id INT REFERENCES carts(cart_id),
    order_status_order_status_id INT REFERENCES order_status(order_status_id),
    shipping_total DECIMAL,
    total DECIMAL,
    created_at TIMESTAMP(2),
    updated_at TIMESTAMP(2)
);
COPY orders FROM '/usr/src/orders.csv' DELIMITER ',';

CREATE TABLE categories(
    category_id SERIAL PRIMARY KEY,
    category_title VARCHAR(255),
    category_description TEXT
);
COPY categories FROM '/usr/src/categories.csv' DELIMITER ',';

CREATE TABLE products(
    product_id SERIAL PRIMARY KEY,
    product_title VARCHAR(255),
    product_description TEXT,
    in_stock INT,
    price FLOAT,
    slug VARCHAR(45),
    category_id INT REFERENCES categories(category_id)
);
COPY products FROM '/usr/src/products.csv' DELIMITER ',';

CREATE TABLE cart_product(
    carts_cart_id INT REFERENCES carts(cart_id),
    products_product_id INT REFERENCES products(product_id)
);
COPY cart_product FROM '/usr/src/cart_products.csv' DELIMITER ',';


-- 2 task
ALTER TABLE users
ADD COLUMN phone_number INT;

ALTER TABLE users
ALTER COLUMN phone_number
SET DATA TYPE VARCHAR(15);

-- 3 task
UPDATE products
SET price = price * 2
