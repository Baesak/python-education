-- task 1
-- Вывести:
-- 1. всех юзеров,
-- 2. все продукты,
-- 3. все статусы заказов

SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM order_status;

-- task 2
-- Вывести заказы, которые успешно доставлены и оплачены

SELECT * FROM orders
WHERE order_status_order_status_id = 4;

-- task 3
-- Вывести:
-- (если задание можно решить несколькими способами, указывай все)
-- 1. Продукты, цена которых больше 80.00 и меньше или равно 150.00
-- 2. заказы совершенные после 01.10.2020 (поле created_at)
-- 3. заказы полученные за первое полугодие 2020 года
-- 4. подукты следующих категорий Category 7, Category 11, Category 18
-- 5. незавершенные заказы по состоянию на 31.12.2020
-- 6.Вывести все корзины, которые были созданы, но заказ так и не был оформлен.

SELECT * FROM products
WHERE price > 80.00 AND price <= 150.00;

SELECT * FROM orders
WHERE created_at > '2020-10-01';

SELECT * FROM orders
WHERE created_at >= '2020-01-01' AND created_at < '2020-06-01';

SELECT * FROM products
WHERE category_id IN (7, 11, 18);

SELECT * FROM orders
WHERE created_at < '2020-12-31' AND order_status_order_status_id NOT IN (4, 5);

SELECT * FROM carts
WHERE cart_id NOT IN(
    SELECT carts_cart_id FROM orders
    );

--task 4
-- Вывести:
-- 1. среднюю сумму всех завершенных сделок
-- 2. вывести максимальную сумму сделки за 3 квартал 2020

SELECT AVG(total) FROM orders
WHERE order_status_order_status_id = 4;

SELECT MAX(total) FROM orders
WHERE order_status_order_status_id = 4
AND '2021-01-19' > created_at  AND created_at >= '2020-10-19'