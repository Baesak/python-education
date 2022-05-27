CREATE OR REPLACE FUNCTION change_shipping_total(check_city varchar(255))
returns numeric
language plpgsql
AS
$$
DECLARE
    city_exist VARCHAR(255);
    shipping_total_sum numeric;

BEGIN

    SELECT u.city INTO city_exist FROM users
    JOIN users u ON u.city = check_city
    LIMIT 1;

    if city_exist is null then
        raise 'There is no user with city %', check_city;
    end if;

    UPDATE orders SET shipping_total = 0 WHERE order_id in
    (SELECT o.order_id FROM users
    JOIN users u ON u.city = check_city
    JOIN carts ON u.user_id = carts.user_id
    JOIN orders o ON o.carts_cart_id = carts.cart_id);

    SELECT SUM(shipping_total) INTO shipping_total_sum FROM orders;

    return shipping_total_sum;
end;$$;

SELECT * FROM change_shipping_total('city 2');


--- Removes product from specified cart if price of the product is more than price limit.
CREATE OR REPLACE procedure remove_to_expensive (price_limit int, cart_id int)
language plpgsql
AS
$$
DECLARE
    row record;
BEGIN
    for row in (SELECT p.product_id, p.price FROM products
                JOIN cart_product ON carts_cart_id = cart_id
                JOIN products p ON cart_product.products_product_id = p.product_id)
    LOOP
        if row.price >= price_limit then
            DELETE FROM cart_product WHERE products_product_id = row.product_id and carts_cart_id = cart_id;
        end if;
    end loop;
end;
$$;

CALL remove_to_expensive(1, 1000);

BEGIN;
call remove_to_expensive(1, 1);
SELECT * FROM cart_product;
ROLLBACK;
END;

---Creates new user based on row from potential_costumers row. There is action in my shop! In some cities some products
---cost less. This product will be automatically placed in new users cart.
CREATE OR REPLACE PROCEDURE create_user_from_potential_user(potential_id int)
language plpgsql
AS
$$
DECLARE
    potential_row record;
    new_user_id int;
    new_cart_id int;
    discount_products_id int[];
    total numeric;
    index int;
    discount bool := false;

BEGIN

    SELECT * INTO potential_row FROM potential_customers WHERE id = potential_id;
    SELECT MAX(user_id)+1 INTO new_user_id FROM users;

    INSERT INTO users
    VALUES (new_user_id, potential_row.email, 1234, potential_row.name, potential_row.surname,
    potential_row.second_name, 2, 'some_country', potential_row.city, 'some_address',
    '88005553535');
    DELETE FROM potential_customers WHERE id = potential_id;
    SELECT MAX(user_id) INTO new_user_id FROM users;

    if potential_row.city = 'city 17' then
        discount_products_id = array[1, 4];
        total = 250.0;
        discount = True;

    elsif potential_row.city = 'city 2'then
        discount_products_id = array[14, 2, 16];
        total = 500.0;
        discount = True;

    elsif potential_row.city = 'city 18' then
        discount_products_id = array[14, 2, 16];
        total = 100.0;
        discount = True;

    end if;

    if discount then
        INSERT INTO carts VALUES (new_user_id, total-20, total);
        SELECT MAX(cart_id) INTO new_cart_id FROM carts;

        foreach index in array discount_products_id
        loop
            INSERT INTO cart_product VALUES(new_cart_id, index);
        end loop;
    end if;

end;
$$;

CALL create_user_from_potential_user(7);

---Fills selected cart with specified products. If sum of all product is more than price limit - makes rollback.
CREATE OR REPLACE PROCEDURE fill_cart_with_money_check (cart_id integer, products_id_list integer[],
price_limit int)

language plpgsql
AS
$$
DECLARE
    actual_price_sum int := 0;
    product record;
    index int;
BEGIN

    foreach index in array products_id_list
    loop
        SELECT product_id, price INTO product FROM products;
        actual_price_sum = actual_price_sum + product.price;
        if actual_price_sum >= price_limit then
            ROLLBACK;
        end if;

        INSERT INTO cart_product VALUES (cart_id, product.product_id);
        actual_price_sum = actual_price_sum + product.product_id;

    end loop;

end;
$$;

CALL fill_cart_with_money_check(4, array[16, 2], 1000);
CALL fill_cart_with_money_check(30, array[20, 3, 21], 10);
