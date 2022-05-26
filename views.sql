--- For Products

CREATE VIEW products_by_popularity AS
    SELECT COUNT(products_product_id) AS use_in_orders_amount, products_product_id FROM cart_product
    INNER JOIN orders ON cart_product.carts_cart_id = orders.carts_cart_id
    GROUP BY products_product_id
    ORDER BY use_in_orders_amount DESC;

SELECT * FROM products_by_popularity
LIMIT 10;

DROP VIEW products_by_popularity CASCADE;


CREATE VIEW most_popular_product AS
    SELECT products_product_id as most_popular_product FROM products_by_popularity
    LIMIT 1;

SELECT * FROM most_popular_product;

DROP VIEW most_popular_product;


CREATE VIEW price_for_full_amount AS
    SELECT product_id, product_title, (price * in_stock) AS price_for_full_amount FROM products
    WHERE in_stock > 0;

SELECT * FROM price_for_full_amount;

DROP VIEW price_for_full_amount;


--- For Products & Category

CREATE VIEW product_more_info AS
    SELECT product_id, product_title, product_description, category_id, category_title, category_description
    FROM products
    JOIN categories USING (category_id);

SELECT * FROM product_more_info;

DROP VIEW product_more_info;


CREATE VIEW amount_products_in_categories AS
    SELECT COUNT(products_product_id) as products_amount, products.category_id
    FROM cart_product
    JOIN products ON products.product_id = cart_product.products_product_id
    GROUP BY products.category_id
    ORDER BY products_amount;

SELECT * FROM amount_products_in_categories;

DROP VIEW amount_products_in_categories;


CREATE VIEW most_expensive_categories AS
    SELECT avg(price) AS price_of_all_products, category_id FROM products
    GROUP BY category_id
    ORDER BY price_of_all_products DESC;

SELECT * FROM most_expensive_categories;

DROP VIEW most_expensive_categories;


--- Order Status & Order

CREATE VIEW in_process_orders AS
    SELECT * FROM orders
    JOIN order_status ON order_status_id not in (4, 5);

SELECT * FROM in_process_orders;

DROP VIEW in_process_orders;


CREATE VIEW lost_money AS
    SELECT sum(orders.total) as money_lost FROM orders
    WHERE order_status_order_status_id = 4;

SELECT * FROM lost_money;

DROP VIEW lost_money;


CREATE VIEW amount_of_each_status AS
    SELECT COUNT(order_id) AS orders_amount, order_status_id FROM orders
    JOIN order_status ON orders.order_status_order_status_id = order_status.order_status_id
    GROUP BY order_status_id;

SELECT * FROM amount_of_each_status ORDER BY orders_amount;

DROP VIEW amount_of_each_status;


--- Materialized

CREATE MATERIALIZED VIEW hard_query AS
    SELECT * FROM users
    JOIN carts USING (user_id)
    JOIN cart_product cp ON carts.cart_id = cp.carts_cart_id
    JOIN products ON cp.products_product_id = products.product_id
    JOIN categories USING(category_id);

SELECT * FROM hard_query;

DROP MATERIALIZED VIEW hard_query
