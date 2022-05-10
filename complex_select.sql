
-- Задание 1
-- Создайте новую таблицу potential customers с полями id, email, name, surname, second_name, city
-- Заполните данными таблицу.
-- Выведите имена и электронную почту потенциальных и существующих пользователей из города city 17

CREATE TABLE potential_customers(
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255),
    surname VARCHAR(255),
    second_name VARCHAR(255),
    city VARCHAR(255)
);

INSERT INTO potential_customers VALUES
    (1, 'example@gmail.com', 'name1', 'surname1', 'second_name1', 'city 11'),
    (2, 'example2@gmail.com', 'name2', 'surname2', 'second_name2', 'city 12'),
    (3, 'example3@gmail.com', 'name3', 'surname3', 'second_name3', 'city 13'),
    (4, 'example4@gmail.com', 'name4', 'surname4', 'second_name4', 'city 14'),
    (5, 'example5@gmail.com', 'name5', 'surname5', 'second_name5', 'city 15'),
    (6, 'example6@gmail.com', 'name6', 'surname6', 'second_name6', 'city 16'),
    (7, 'example7@gmail.com', 'name7', 'surname7', 'second_name7', 'city 17'),
    (8, 'example8@gmail.com', 'name8', 'surname8', 'second_name8', 'city 17'),
    (9, 'example9@gmail.com', 'name9', 'surname9', 'second_name9', 'city 17');

SELECT name, surname FROM potential_customers
WHERE city = 'city 17'
UNION
SELECT first_name, last_name FROM users
WHERE city = 'city 17';


-- Задание 2
-- Вывести имена и электронные адреса всех users отсортированных по городам и по имени (по алфавиту)
SELECT first_name, last_name, email FROM users
ORDER BY first_name, email;

-- Задание 3
-- Вывести наименование группы товаров, общее количество по группе товаров в порядке убывания количества

SELECT COUNT(product_id) as product_amount, category_title FROM products
JOIN categories on products.category_id = categories.category_id
GROUP BY category_title
ORDER BY product_amount DESC;

-- Задание 4
-- 1. Вывести продукты, которые ни разу не попадали в корзину.
-- 2. Вывести все продукты, которые так и не попали ни в 1 заказ. (но в корзину попасть могли).
-- 3. Вывести топ 10 продуктов, которые добавляли в корзины чаще всего.
-- 4. Вывести топ 10 продуктов, которые не только добавляли в корзины, но и оформляли заказы чаще всего.
-- 5. Вывести топ 5 юзеров, которые потратили больше всего денег (total в заказе).
-- 6. Вывести топ 5 юзеров, которые сделали больше всего заказов (кол-во заказов).
-- 7. Вывести топ 5 юзеров, которые создали корзины, но так и не сделали заказы.

SELECT product_title FROM products
LEFT JOIN cart_product ON products.product_id = cart_product.products_product_id
WHERE products_product_id is null;

SELECT products_product_id FROM cart_product
LEFT JOIN orders ON cart_product.carts_cart_id = orders.carts_cart_id
WHERE orders.carts_cart_id IS null;

SELECT COUNT(products_product_id) AS use_amount, products_product_id FROM cart_product
GROUP BY products_product_id
ORDER BY use_amount DESC
LIMIT 10;

SELECT COUNT(products_product_id) AS use_in_orders_amount, products_product_id FROM cart_product
INNER JOIN orders ON cart_product.carts_cart_id = orders.carts_cart_id
GROUP BY products_product_id
ORDER BY use_in_orders_amount DESC
LIMIT 10;

SELECT carts.user_id, orders.total FROM orders
JOIN carts ON carts.cart_id = orders.carts_cart_id
WHERE order_status_order_status_id = 4
ORDER BY total DESC
LIMIT 5;

SELECT carts.user_id, orders.total FROM orders
JOIN carts ON carts.cart_id = orders.carts_cart_id
WHERE order_status_order_status_id = 4
ORDER BY total DESC
LIMIT 5;

SELECT COUNT(user_id) as amount_of_orders, user_id FROM orders
JOIN carts ON carts.cart_id = orders.carts_cart_id
WHERE order_status_order_status_id = 4
GROUP BY user_id
ORDER BY amount_of_orders DESC
LIMIT 5;

SELECT COUNT(user_id) as amount_of_carts, user_id FROM orders
RIGHT JOIN carts ON carts.cart_id = orders.carts_cart_id
WHERE orders.carts_cart_id IS NULL
GROUP BY user_id
ORDER BY amount_of_carts DESC
LIMIT 5;