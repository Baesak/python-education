CREATE OR REPLACE FUNCTION random_between(low INT ,high INT)
   RETURNS INT AS
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;
$$ language 'plpgsql' STRICT;

INSERT INTO categories
SELECT id, random()::VARCHAR(255), random()::VARCHAR(255) FROM generate_series(21, 15000) AS id;

INSERT INTO products
SELECT id, random()::VARCHAR(255), random()::text, random_between(1, 5000), random()::double precision,
       random()::VARCHAR(45), random_between(1, 15000) FROM generate_series(4001, 15000) AS id;


-- Hash Join  (cost=10000000888.96..10000001424.35 rows=15000 width=116) (actual time=415.680..632.175 rows=15000 loops=1)
--   Hash Cond: (products.category_id = categories.category_id)
--   ->  Seq Scan on products  (cost=10000000000.00..10000000496.00 rows=15000 width=74) (actual time=0.051..71.743 rows=15000 loops=1)
--   ->  Hash  (cost=701.46..701.46 rows=15000 width=42) (actual time=415.547..415.567 rows=15000 loops=1)
--         Buckets: 16384  Batches: 1  Memory Usage: 1220kB
--         ->  Index Scan using categories_pkey on categories  (cost=0.29..701.46 rows=15000 width=42) (actual time=0.055..76.889 rows=15000 loops=1)
-- Planning Time: 0.618 ms
-- JIT:
--   Functions: 10
-- "  Options: Inlining true, Optimization true, Expressions true, Deforming true"
-- "  Timing: Generation 7.387 ms, Inlining 17.360 ms, Optimization 147.188 ms, Emission 99.170 ms, Total 271.104 ms"
-- Execution Time: 710.067 ms


CREATE INDEX products_category_id ON products(category_id);

EXPLAIN ANALYSE
SELECT * FROM products
JOIN categories ON products.category_id = categories.category_id;

-- Merge Join  (cost=0.57..2310.16 rows=15000 width=116) (actual time=0.068..378.656 rows=15000 loops=1)
--   Merge Cond: (products.category_id = categories.category_id)
--   ->  Index Scan using products_category_id on products  (cost=0.29..1383.70 rows=15000 width=74) (actual time=0.025..84.545 rows=15000 loops=1)
--   ->  Index Scan using categories_pkey on categories  (cost=0.29..701.46 rows=15000 width=42) (actual time=0.020..73.668 rows=15000 loops=1)
-- Planning Time: 0.323 ms
-- Execution Time: 451.619 ms




-- Hash Join  (cost=478.50..1022.34 rows=3939 width=116) (actual time=145.898..204.312 rows=4000 loops=1)
--   Hash Cond: (products.category_id = categories.category_id)
--   ->  Seq Scan on products  (cost=0.00..533.50 rows=3939 width=74) (actual time=0.066..20.605 rows=4000 loops=1)
--         Filter: ((product_title)::text ~~ 'Prod%'::text)
--         Rows Removed by Filter: 11000
--   ->  Hash  (cost=291.00..291.00 rows=15000 width=42) (actual time=145.784..145.799 rows=15000 loops=1)
--         Buckets: 16384  Batches: 1  Memory Usage: 1220kB
--         ->  Seq Scan on categories  (cost=0.00..291.00 rows=15000 width=42) (actual time=0.015..71.427 rows=15000 loops=1)
-- Planning Time: 0.548 ms
-- Execution Time: 223.103 ms

CREATE INDEX product_title ON products(product_title);

EXPLAIN ANALYSE
SELECT * FROM products
JOIN categories ON products.category_id = categories.category_id
WHERE product_title LIKE 'Prod%';

-- Merge Join  (cost=0.57..2209.40 rows=3939 width=116) (actual time=0.056..75.084 rows=4000 loops=1)
--   Merge Cond: (products.category_id = categories.category_id)
--   ->  Index Scan using products_category_id on products  (cost=0.29..1421.20 rows=3939 width=74) (actual time=0.022..33.044 rows=4000 loops=1)
--         Filter: ((product_title)::text ~~ 'Prod%'::text)
--         Rows Removed by Filter: 11000
--   ->  Index Scan using categories_pkey on categories  (cost=0.29..701.46 rows=15000 width=42) (actual time=0.016..0.127 rows=20 loops=1)
-- Planning Time: 0.279 ms
-- Execution Time: 96.901 ms

-- Hash Join  (cost=1222.02..1466.26 rows=10918 width=152) (actual time=309.761..679.799 rows=10995 loops=1)
--   Hash Cond: (cart_product.carts_cart_id = carts.cart_id)
--   ->  Hash Join  (cost=1162.00..1377.52 rows=10918 width=124) (actual time=288.651..553.775 rows=10995 loops=1)
--         Hash Cond: (products.category_id = categories.category_id)
--         ->  Hash Join  (cost=683.50..870.35 rows=10918 width=82) (actual time=141.974..302.056 rows=10995 loops=1)
--               Hash Cond: (cart_product.products_product_id = products.product_id)
--               ->  Seq Scan on cart_product  (cost=0.00..158.18 rows=10918 width=8) (actual time=0.016..52.191 rows=10995 loops=1)
--               ->  Hash  (cost=496.00..496.00 rows=15000 width=74) (actual time=141.921..141.936 rows=15000 loops=1)
--                     Buckets: 16384  Batches: 1  Memory Usage: 1753kB
--                     ->  Seq Scan on products  (cost=0.00..496.00 rows=15000 width=74) (actual time=0.035..70.384 rows=15000 loops=1)
--         ->  Hash  (cost=291.00..291.00 rows=15000 width=42) (actual time=146.640..146.654 rows=15000 loops=1)
--               Buckets: 16384  Batches: 1  Memory Usage: 1220kB
--               ->  Seq Scan on categories  (cost=0.00..291.00 rows=15000 width=42) (actual time=0.024..73.224 rows=15000 loops=1)
--   ->  Hash  (cost=35.01..35.01 rows=2001 width=28) (actual time=21.086..21.099 rows=2001 loops=1)
--         Buckets: 2048  Batches: 1  Memory Usage: 142kB
--         ->  Seq Scan on carts  (cost=0.00..35.01 rows=2001 width=28) (actual time=0.022..9.845 rows=2001 loops=1)
-- Planning Time: 1.165 ms
-- Execution Time: 731.035 ms


CREATE INDEX cart_product_product ON cart_product(products_product_id);
CREATE INDEX cart_product_cart ON cart_product(carts_cart_id);

EXPLAIN ANALYSE
SELECT * FROM products
JOIN categories ON products.category_id = categories.category_id
JOIN cart_product ON cart_product.products_product_id = products.product_id
JOIN carts ON cart_id = cart_product.carts_cart_id


-- Hash Join  (cost=106.17..1828.20 rows=10995 width=152) (actual time=20.328..424.790 rows=10995 loops=1)
--   Hash Cond: (cart_product.carts_cart_id = carts.cart_id)
--   ->  Merge Join  (cost=0.87..1693.98 rows=10995 width=124) (actual time=0.091..294.536 rows=10995 loops=1)
--         Merge Cond: (products.product_id = cart_product.products_product_id)
--         ->  Nested Loop  (cost=0.58..4098.41 rows=15000 width=116) (actual time=0.058..104.185 rows=4001 loops=1)
--               ->  Index Scan using products_pkey on products  (cost=0.29..886.28 rows=15000 width=74) (actual time=0.019..20.403 rows=4001 loops=1)
--               ->  Memoize  (cost=0.30..0.37 rows=1 width=42) (actual time=0.005..0.005 rows=1 loops=4001)
--                     Cache Key: products.category_id
--                     Cache Mode: logical
--                     Hits: 3980  Misses: 21  Evictions: 0  Overflows: 0  Memory Usage: 3kB
--                     ->  Index Scan using categories_pkey on categories  (cost=0.29..0.36 rows=1 width=42) (actual time=0.052..0.052 rows=1 loops=21)
--                           Index Cond: (category_id = products.category_id)
--         ->  Index Scan using cart_product_product on cart_product  (cost=0.29..453.21 rows=10995 width=8) (actual time=0.018..61.977 rows=10995 loops=1)
--   ->  Hash  (cost=80.29..80.29 rows=2001 width=28) (actual time=20.210..20.224 rows=2001 loops=1)
--         Buckets: 2048  Batches: 1  Memory Usage: 142kB
--         ->  Index Scan using carts_pkey on carts  (cost=0.28..80.29 rows=2001 width=28) (actual time=0.014..10.409 rows=2001 loops=1)
-- Planning Time: 0.865 ms
-- Execution Time: 478.065 ms
-- Hash Join  (cost=106.17..1828.20 rows=10995 width=152) (actual time=20.328..424.790 rows=10995 loops=1)
--   Hash Cond: (cart_product.carts_cart_id = carts.cart_id)
--   ->  Merge Join  (cost=0.87..1693.98 rows=10995 width=124) (actual time=0.091..294.536 rows=10995 loops=1)
--         Merge Cond: (products.product_id = cart_product.products_product_id)
--         ->  Nested Loop  (cost=0.58..4098.41 rows=15000 width=116) (actual time=0.058..104.185 rows=4001 loops=1)
--               ->  Index Scan using products_pkey on products  (cost=0.29..886.28 rows=15000 width=74) (actual time=0.019..20.403 rows=4001 loops=1)
--               ->  Memoize  (cost=0.30..0.37 rows=1 width=42) (actual time=0.005..0.005 rows=1 loops=4001)
--                     Cache Key: products.category_id
--                     Cache Mode: logical
--                     Hits: 3980  Misses: 21  Evictions: 0  Overflows: 0  Memory Usage: 3kB
--                     ->  Index Scan using categories_pkey on categories  (cost=0.29..0.36 rows=1 width=42) (actual time=0.052..0.052 rows=1 loops=21)
--                           Index Cond: (category_id = products.category_id)
--         ->  Index Scan using cart_product_product on cart_product  (cost=0.29..453.21 rows=10995 width=8) (actual time=0.018..61.977 rows=10995 loops=1)
--   ->  Hash  (cost=80.29..80.29 rows=2001 width=28) (actual time=20.210..20.224 rows=2001 loops=1)
--         Buckets: 2048  Batches: 1  Memory Usage: 142kB
--         ->  Index Scan using carts_pkey on carts  (cost=0.28..80.29 rows=2001 width=28) (actual time=0.014..10.409 rows=2001 loops=1)
-- Planning Time: 0.865 ms
-- Execution Time: 478.065 ms

