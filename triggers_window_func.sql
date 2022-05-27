--- 1

SELECT category_title, product_title, price,
AVG(price) OVER(PARTITION BY category_id)
FROM products
JOIN categories USING (category_id);

--- 2
--- Check users email and phone after creation.
CREATE OR REPLACE FUNCTION check_user_creation()
returns TRIGGER
language plpgsql
AS
$$
BEGIN
    if regexp_match(NEW.email, '^(.+)@(.+)$') is null then
        raise 'Email format is wrong %', new.email;
    elseif regexp_match(NEW.phone_number, '^[0-9-+\s]+$') is null then
        raise 'Wrong number format!';
    end if;
END;
$$;

CREATE TRIGGER user_validation
    BEFORE INSERT
    ON users
    FOR EACH ROW
    EXECUTE PROCEDURE check_user_creation();


INSERT INTO users VALUES ((SELECT MAX(user_id)+1 from users), 'salhdhldasklh', 21331, 's', 's', 's', 3,
                          's', 's', 's', +1332331213);
INSERT INTO users VALUES ((SELECT MAX(user_id)+1 from users), 'user@domain.com', 2222, 's', 's', 's', 3,
                          's', 's', '54');


--- Makes 30% discount on total price of products in cart if today is black friday.
CREATE OR REPLACE FUNCTION black_friday_discount()
returns TRIGGER
language plpgsql
AS
$$
BEGIN
    if to_char(now(), 'DD-MM') = '05-11' then
        NEW.total = NEW.total * (30/100);
    end if;
END;
$$;


CREATE TRIGGER black_friday_discount
    AFTER INSERT
    ON carts
    FOR EACH ROW
    EXECUTE PROCEDURE black_friday_discount();
