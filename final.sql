CREATE DATABASE car_sharing;

CREATE TABLE customer(
    id SERIAL PRIMARY KEY ,
    first_name VARCHAR(250),
    last_name VARCHAR(250),
    address_id INT REFERENCES address ON DELETE CASCADE,
    phone_number_id INT REFERENCES phone_number ON DELETE CASCADE
 );
call fill_customer(10000);

CREATE TABLE city(
    id SERIAL PRIMARY KEY,
    city VARCHAR(250)
);
call fill_city(10000);

CREATE TABLE address(
    id SERIAL PRIMARY KEY,
    city_id int REFERENCES city ON DELETE CASCADE ,
    address VARCHAR(250)
);

call fill_address(10000);


CREATE TABLE branch(
    number INT PRIMARY KEY,
    address_id INT REFERENCES address ON DELETE CASCADE ,
    phone_number_id INT REFERENCES phone_number ON DELETE CASCADE
);
call fill_branch(10000);

CREATE TABLE manufacturer(
    id SERIAL PRIMARY KEY,
    manufacturer VARCHAR(250)
);
call fill_manufacturer(10000);


CREATE TABLE car_model(
    id SERIAL PRIMARY KEY,
    manufacturer_id INT REFERENCES manufacturer ON DELETE CASCADE,
    model VARCHAR(250)
);
call fill_car_model(10000);

CREATE TABLE car(
    id SERIAL PRIMARY KEY,
    number VARCHAR(8) UNIQUE,
    price_per_day INT NOT NULL ,
    car_model_id INT REFERENCES car_model ON DELETE CASCADE ,
    branch_number INT REFERENCES branch ON DELETE CASCADE
);
call fill_car(10000);

CREATE TABLE phone_number(
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(250)
);
call fill_phone_number(10000);

CREATE TABLE rent(
    id SERIAL PRIMARY KEY,
    price INT,
    date_of_rent DATE NOT NULL ,
    car_id INT REFERENCES car ON DELETE CASCADE,
    renting_due DATE,
    customer_id INT REFERENCES customer ON DELETE CASCADE
);

call fill_rent(10000);

CREATE TABLE car_audit(
    car_number VARCHAR(8),
    car_model_id INT,
    date_of_deleting DATE,
    car_brunch_number INT
);


---FUNCTIONS

CREATE OR REPLACE FUNCTION random_between(low INT ,high INT)
returns INT
language plpgsql
AS
$$
BEGIN
   RETURN floor(random() * (high-low + 1) + low);
END;
$$;

--- RETURNING TABLE
--- Returns all cars prices with specified discount.
CREATE OR REPLACE FUNCTION cars_with_discount(percents int)
returns table(car_number VARCHAR(8), price_per_day int, discount VARCHAR(4))
language plpgsql
AS
$$
BEGIN
    return query SELECT number, price_per_day * (percents/100), percents::char || '%' FROM car;
END;
$$;


--- CYCLE
CREATE OR REPLACE FUNCTION generate_phone_number()
returns VARCHAR(10)
language plpgsql
AS
$$
DECLARE
    new_phone_number VARCHAR(10) := '+0';
BEGIN
   WHILE length(new_phone_number) <> 10
    loop
       new_phone_number = new_phone_number || random_between(0, 9)::CHAR;
    end loop;

   return new_phone_number;

END;
$$;

--- CURSOR
--- Returns string with full customers names before specified costumer, with name of that customer included.
CREATE OR REPLACE FUNCTION string_all_customers_before(customer_id int)
returns text
language plpgsql
AS
$$
DECLARE
    names TEXT;
    full_name record;
    cur_customers CURSOR FOR SELECT first_name, last_name FROM customer;
BEGIN

    SELECT first_name || last_name INTO names FROM customer;
    if names = (SELECT first_name || last_name FROM customer WHERE id = customer_id) then
        return names;
    end if;

    open cur_customers;
    loop
        fetch cur_customers into full_name;
        exit when not found;

        names = names || (full_name.first_name || full_name.last_name);
        if names = (SELECT first_name || last_name FROM customer WHERE id = customer_id) then
        return names;
        end if;
    end loop;
    close cur_customers;

END;
$$;

CREATE OR REPLACE FUNCTION random_2_uppercase_letters()
returns VARCHAR(2)
language plpgsql
as
$$
DECLARE
    chars VARCHAR(1)[] := '{A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z}';
BEGIN
    return chars[random_between(1, array_length(chars, 1))] ||
           chars[random_between(1, array_length(chars, 1))];
end;
$$;

CREATE OR REPLACE FUNCTION generate_number()
returns VARCHAR(8)
language plpgsql
as
$$
DECLARE
    new_number VARCHAR(8);
BEGIN
    new_number = random_2_uppercase_letters() || random_between(0, 9)::VARCHAR(1) ||
    random_between(0, 9)::VARCHAR(1) || random_between(0, 9)::VARCHAR(1) ||
    random_between(0, 9)::VARCHAR(1) || random_2_uppercase_letters();

    return new_number;
end;
$$;


CREATE OR REPLACE FUNCTION id_loop(max_id int)
returns SETOF INT
language plpgsql
as
$$
DECLARE
    id_record int := 1;
BEGIN

    WHILE id_record <= max_id LOOP
        return NEXT id_record;
        id_record = id_record + 1;
        end loop;
end;
$$;

--- PROCEDURES

--- INSERT
CREATE OR REPLACE PROCEDURE fill_manufacturer (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO manufacturer
    SELECT id, md5(random()::VARCHAR(250)) FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_customer (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO customer
    SELECT id, md5(random()::VARCHAR(250)), md5(random()::VARCHAR(250)),
    random_between(1, (SELECT MAX(id) FROM address)),
    random_between(1, (SELECT MAX(id) FROM phone_number))
    FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_phone_number (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO phone_number
    SELECT id, (SELECT generate_phone_number()) FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_city (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO city
    SELECT id, md5(random()::VARCHAR(250)) FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_address (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO address
    SELECT id, random_between(1, (SELECT MAX(id) FROM city)),
           md5(random()::VARCHAR(250)) FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_car_model(values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO car_model
    SELECT id, random_between(1, (SELECT MAX(id) FROM manufacturer)),
           md5(random()::VARCHAR(250)) FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_branch (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO branch
    SELECT id, random_between(1, (SELECT MAX(id) FROM address)),
           random_between(1, (SELECT MAX(id) FROM phone_number))FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_car (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO car
    SELECT id, generate_number(), random_between(100, 10000),
           random_between(1, (SELECT MAX(id) FROM car_model)),
           random_between(1, (SELECT MAX(branch.number) FROM branch))
           FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

CREATE OR REPLACE PROCEDURE fill_rent (values_amount int)
LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO rent
    SELECT id, NULL,
           to_char(timestamp '2022-12-31' + random() * (timestamp '2022-01-01' - timestamp '2022-12-31'),
           'YYYY-MM-DD')::DATE, random_between(1, (SELECT MAX(id) FROM car)), NULL,
           random_between(1, (SELECT MAX(id) FROM customer)) FROM id_loop(values_amount) AS id;
    COMMIT;
end;
$$;

--- UPDATE, DELETE

--- Moves all cars from branch to other branch. If no other brunch specified just deletes all car from branch.
CREATE OR REPLACE PROCEDURE move_cars(old_brunch_number int, new_branch_number int DEFAULT null)
LANGUAGE plpgsql
AS
$$
BEGIN
    if new_branch_number is null then
        DELETE FROM car WHERE branch_number = old_brunch_number;
    else
        UPDATE car SET branch_number = new_branch_number WHERE branch_number = old_brunch_number;
    end if;

    COMMIT;
END;
$$;

SELECT number, branch_number FROM car WHERE branch_number = 1;
SELECT number, branch_number FROM car WHERE branch_number = 3;
call move_cars(1, 3);

---TRIGGERS

CREATE OR REPLACE FUNCTION validate_phone_number()
returns TRIGGER
language plpgsql
AS
$$
BEGIN
    if regexp_match(NEW.phone_number, '^\+?\d+$') is null then
        raise 'Wrong number format!';
    end if;

    return NEW;
end;
$$;

CREATE TRIGGER phone_number_validation
    BEFORE INSERT
    ON phone_number
    FOR EACH ROW
    EXECUTE PROCEDURE validate_phone_number();


CREATE OR REPLACE FUNCTION insert_into_car_audit()
returns TRIGGER
language plpgsql
AS
$$
BEGIN
    INSERT INTO car_audit VALUES (OLD.number, OLD.car_model_id, NOW(), OLD.branch_number);

    return NULL;
end;
$$;


CREATE TRIGGER car_audit_on_delete
    AFTER DELETE
    ON car
    FOR EACH ROW
    EXECUTE PROCEDURE insert_into_car_audit();


CREATE OR REPLACE FUNCTION set_rent_price_and_due_rent()
returns TRIGGER
language plpgsql
AS
$$
DECLARE
    car_price int;
BEGIN
    if NEW.renting_due is null then
        NEW.renting_due = to_char(NEW.date_of_rent + random() * (timestamp '2022-12-31' - NEW.date_of_rent),
            'YYYY-MM-DD')::DATE;
    end if;

    if NEW.price is null then
        SELECT c.price_per_day INTO car_price FROM car
        JOIN car c USING (number);
        NEW.price = car_price * (new.renting_due - NEW.date_of_rent);
    end if;

    return NEW;
END;
$$;

--- Sets price of rent depending of price of car per day. Also sets random due date if it was null.
CREATE TRIGGER set_rent_price
    BEFORE INSERT
    ON rent
    FOR EACH ROW
    EXECUTE PROCEDURE set_rent_price_and_due_rent();


--- VIEWS
--- Makes top cars by amount of renting. Counts amount of renting, shows model and number
CREATE VIEW cars_by_popularity AS
    SELECT COUNT(car_id) AS renting_amount, model, number FROM rent
    JOIN car ON car_id = car.id
    JOIN car_model cm on car.car_model_id = cm.id
    GROUP BY (model, number)
    ORDER BY renting_amount DESC;

SELECT * FROM cars_by_popularity;

--- Selecting most cheap car, how much times it was rented, it's model, manufacturer and price per day.
CREATE MATERIALIZED VIEW most_cheap_car AS
    SELECT (SELECT COUNT(car_id) FROM rent WHERE car_id = c.id) AS amount_of_renting,
           cm.model, cm.manufacturer_id, c.price_per_day FROM car
    JOIN car c ON c.price_per_day = (SELECT MIN(car.price_per_day) FROM car)
    JOIN car_model cm ON c.car_model_id = cm.id
    JOIN rent ON c.id = rent.car_id;

SELECT * FROM most_cheap_car;

--- Show branches with amount of cars in them
CREATE VIEW branches_by_car_amount AS
    SELECT COUNT(car.number) as car_amount, a.address, b.number FROM car
    JOIN branch b on b.number = car.branch_number
    JOIN address a on b.address_id = a.id
    GROUP BY (branch_number, a.address, b.number);

SELECT * FROM branches_by_car_amount;

--
-- Nested Loop  (cost=199.29..838.62 rows=20000 width=41) (actual time=4.059..22.735 rows=20000 loops=1)
--   InitPlan 1 (returns $0)
--     ->  Aggregate  (cost=199.00..199.01 rows=1 width=4) (actual time=3.194..3.196 rows=1 loops=1)
--           ->  Seq Scan on car car_1  (cost=0.00..174.00 rows=10000 width=4) (actual time=0.003..1.447 rows=10000 loops=1)
--   ->  Seq Scan on car  (cost=0.00..174.00 rows=10000 width=0) (actual time=0.009..1.844 rows=10000 loops=1)
--   ->  Materialize  (cost=0.29..215.62 rows=2 width=41) (actual time=0.001..0.001 rows=2 loops=10000)
--         ->  Nested Loop  (cost=0.29..215.61 rows=2 width=41) (actual time=4.043..4.929 rows=2 loops=1)
--               ->  Seq Scan on car c  (cost=0.00..199.00 rows=2 width=8) (actual time=4.021..4.890 rows=2 loops=1)
--                     Filter: (price_per_day = $0)
--                     Rows Removed by Filter: 9998
--               ->  Index Scan using car_model_pkey on car_model cm  (cost=0.29..8.30 rows=1 width=41) (actual time=0.013..0.013 rows=1 loops=2)
--                     Index Cond: (id = c.car_model_id)
-- Planning Time: 0.506 ms
-- Execution Time: 63.420 ms

CREATE INDEX car_car_model_id ON car(car_model_id);
CREATE INDEX car_price ON car(price_per_day);

SET enable_seqscan = 'off';

EXPLAIN ANALYSE
SELECT cm.model, cm.manufacturer_id, c.price_per_day FROM car
    JOIN car c ON c.price_per_day = (SELECT MAX(car.price_per_day) FROM car)
    JOIN car_model cm ON c.car_model_id = cm.id;

-- Nested Loop  (cost=4.91..452.27 rows=20000 width=41) (actual time=0.058..14.966 rows=20000 loops=1)
--   InitPlan 2 (returns $1)
--     ->  Result  (cost=0.31..0.32 rows=1 width=4) (actual time=0.029..0.031 rows=1 loops=1)
--           InitPlan 1 (returns $0)
--             ->  Limit  (cost=0.29..0.31 rows=1 width=4) (actual time=0.026..0.028 rows=1 loops=1)
--                   ->  Index Only Scan Backward using car_price on car car_1  (cost=0.29..279.29 rows=10000 width=4) (actual time=0.026..0.026 rows=1 loops=1)
--                         Index Cond: (price_per_day IS NOT NULL)
--                         Heap Fetches: 0
--   ->  Seq Scan on car  (cost=0.00..174.00 rows=10000 width=0) (actual time=0.005..1.633 rows=10000 loops=1)
--   ->  Materialize  (cost=4.59..27.96 rows=2 width=41) (actual time=0.000..0.000 rows=2 loops=10000)
--         ->  Nested Loop  (cost=4.59..27.95 rows=2 width=41) (actual time=0.048..0.056 rows=2 loops=1)
--               ->  Bitmap Heap Scan on car c  (cost=4.30..11.34 rows=2 width=8) (actual time=0.041..0.044 rows=2 loops=1)
--                     Recheck Cond: (price_per_day = $1)
--                     Heap Blocks: exact=2
--                     ->  Bitmap Index Scan on car_price  (cost=0.00..4.30 rows=2 width=0) (actual time=0.037..0.037 rows=2 loops=1)
--                           Index Cond: (price_per_day = $1)
--               ->  Index Scan using car_model_pkey on car_model cm  (cost=0.29..8.30 rows=1 width=41) (actual time=0.004..0.004 rows=1 loops=2)
--                     Index Cond: (id = c.car_model_id)
-- Planning Time: 0.788 ms
-- Execution Time: 16.439 ms



--
-- Hash Right Join  (cost=359.00..564.26 rows=10000 width=102) (actual time=11.600..41.516 rows=13697 loops=1)
--   Hash Cond: (r.customer_id = customer.id)
--   ->  Seq Scan on rent r  (cost=0.00..179.00 rows=10000 width=24) (actual time=0.023..4.216 rows=10000 loops=1)
--   ->  Hash  (cost=234.00..234.00 rows=10000 width=78) (actual time=11.535..11.538 rows=10000 loops=1)
--         Buckets: 16384  Batches: 1  Memory Usage: 1183kB
--         ->  Seq Scan on customer  (cost=0.00..234.00 rows=10000 width=78) (actual time=0.016..3.710 rows=10000 loops=1)
-- Planning Time: 0.520 ms
-- Execution Time: 44.608 ms

CREATE INDEX rent_customer ON rent(customer_id);

EXPLAIN ANALYSE
SELECT * FROM customer
LEFT JOIN rent r on customer.id = r.customer_id;

-- Merge Left Join  (cost=0.57..1127.57 rows=10000 width=102) (actual time=0.056..27.804 rows=13697 loops=1)
--   Merge Cond: (customer.id = r.customer_id)
--   ->  Index Scan using customer_pkey on customer  (cost=0.29..407.29 rows=10000 width=78) (actual time=0.023..4.497 rows=10000 loops=1)
--   ->  Index Scan using rent_cutomer on rent r  (cost=0.29..570.28 rows=10000 width=24) (actual time=0.023..10.471 rows=10000 loops=1)
-- Planning Time: 0.555 ms
-- Execution Time: 14.279 ms



-- Hash Full Join  (cost=443.86..1537.11 rows=10000 width=78) (actual time=12.921..75.860 rows=13676 loops=1)
--   Hash Cond: (car.branch_number = b.number)
--   ->  Merge Join  (cost=0.57..1067.56 rows=10000 width=66) (actual time=0.060..41.916 rows=10000 loops=1)
--         Merge Cond: (car.car_model_id = cm.id)
--         ->  Index Scan using car_car_model_id on car  (cost=0.29..550.27 rows=10000 width=25) (actual time=0.032..17.873 rows=10000 loops=1)
--         ->  Index Scan using car_model_pkey on car_model cm  (cost=0.29..367.29 rows=10000 width=41) (actual time=0.018..6.638 rows=10000 loops=1)
--   ->  Hash  (cost=318.29..318.29 rows=10000 width=12) (actual time=12.823..12.827 rows=10000 loops=1)
--         Buckets: 16384  Batches: 1  Memory Usage: 519kB
--         ->  Index Scan using branch_pkey on branch b  (cost=0.29..318.29 rows=10000 width=12) (actual time=0.027..6.563 rows=10000 loops=1)
-- Planning Time: 0.760 ms
-- Execution Time: 80.391 ms

CREATE INDEX car_branch ON car(branch_number);

EXPLAIN ANALYSE
SELECT * FROM car
JOIN car_model cm on car.car_model_id = cm.id
FULL OUTER JOIN branch b on car.branch_number = b.number;

-- Hash Full Join  (cost=443.86..1537.11 rows=10000 width=78) (actual time=7.497..39.192 rows=13676 loops=1)
--   Hash Cond: (car.branch_number = b.number)
--   ->  Merge Join  (cost=0.57..1067.56 rows=10000 width=66) (actual time=0.052..20.962 rows=10000 loops=1)
--         Merge Cond: (car.car_model_id = cm.id)
--         ->  Index Scan using car_car_model_id on car  (cost=0.29..550.27 rows=10000 width=25) (actual time=0.027..9.718 rows=10000 loops=1)
--         ->  Index Scan using car_model_pkey on car_model cm  (cost=0.29..367.29 rows=10000 width=41) (actual time=0.015..3.425 rows=10000 loops=1)
--   ->  Hash  (cost=318.29..318.29 rows=10000 width=12) (actual time=7.424..7.427 rows=10000 loops=1)
--         Buckets: 16384  Batches: 1  Memory Usage: 519kB
--         ->  Index Scan using branch_pkey on branch b  (cost=0.29..318.29 rows=10000 width=12) (actual time=0.015..3.768 rows=10000 loops=1)
-- Planning Time: 0.771 ms
-- Execution Time: 35.363 ms

