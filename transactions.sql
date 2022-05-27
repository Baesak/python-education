BEGIN;

INSERT INTO potential_customers VALUES
(10, 'some10_email', 'name10', 'surname10', 'second_name10', 'city18');
SAVEPOINT first_insert;

INSERT INTO potential_customers VALUES
(11, 'some11_email', 'name11', 'surname11', 'second_name11', 'city19');

ROLLBACK TO first_insert;
COMMIT;


BEGIN;

DELETE FROM potential_customers WHERE id = 1;
DELETE FROM potential_customers WHERE id = 4;
DELETE FROM potential_customers WHERE id = 3;

ROLLBACK;
COMMIT;


BEGIN;

SAVEPOINT rollback_update;
UPDATE potential_customers SET city = 'city 71' WHERE city = 'city 17';
UPDATE potential_customers SET name = 'name 82' WHERE name = 'name 10';

ROLLBACK TO rollback_update;
COMMIT;

BEGIN;

INSERT INTO carts VALUES
(5000, 10, 130.12, 300.0),
(5001, 11, 23.30, 56.0),
(5002, 12, 502.12, 700.0);

COMMIT;


BEGIN;

DELETE FROM carts WHERE cart_id = 5000;
DELETE FROM carts WHERE cart_id = 5002;
SAVEPOINT delete_2_cards;
DELETE FROM carts WHERE cart_id = 5003;

ROLLBACK TO delete_2_cards;
COMMIT;


BEGIN;

UPDATE carts SET total = 1000.0 WHERE cart_id = 5003;

COMMIT;


BEGIN;

INSERT INTO categories VALUES
(5000, 'sweet_food', 'Awesome category'),
(5001, 'instruments', 'Awesome category');

SAVEPOINT sweets_and_instruments;

INSERT INTO categories VALUES
(5002, 'cars', 'Cool category');

ROLLBACK TO sweets_and_instruments;
COMMIT;


BEGIN;

UPDATE categories SET category_title = 'Nice category' WHERE category_title = 'Awesome category';
ROLLBACK;

COMMIT;


BEGIN;

DELETE FROM categories WHERE category_title = 'Awesome category';

COMMIT;
