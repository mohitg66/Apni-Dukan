
-- update the delivery address of the order if the delivery address is not provided
DROP TRIGGER IF EXISTS delivery_address;
delimiter //
CREATE TRIGGER delivery_address
BEFORE INSERT ON delivery
FOR EACH ROW
BEGIN
    if (NEW.delivery_address_house_no = NULL AND NEW.delivery_address_city = NULL AND NEW.delivery_address_state = NULL AND NEW.delivery_address_pincode = NULL) THEN
        SET NEW.delivery_address_house_no = (SELECT order_billing_address_house_no FROM orders WHERE order_ID = NEW.order_ID);
        SET NEW.delivery_address_city = (SELECT order_billing_address_city FROM orders WHERE order_ID = NEW.order_ID);
        SET NEW.delivery_address_state = (SELECT order_billing_address_state FROM orders WHERE order_ID = NEW.order_ID);
        SET NEW.delivery_address_pincode = (SELECT order_billing_address_pincode FROM orders WHERE order_ID = NEW.order_ID);
    END IF;
END;//


-- delete the cart records of the customer if the customer has placed an order
DROP TRIGGER IF EXISTS empty_cart;
delimiter //
CREATE TRIGGER empty_cart
AFTER INSERT ON payment
FOR EACH ROW
BEGIN
    DELETE FROM cart WHERE customer_ID = NEW.customer_ID;
END;//

-- update the order_billing_address of the order if the billing address is not provided
DROP TRIGGER IF EXISTS billing_address;
delimiter //
CREATE TRIGGER billing_address
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    if (NEW.order_billing_address_house_no = NULL AND NEW.order_billing_address_city = NULL AND NEW.order_billing_address_state = NULL AND NEW.order_billing_address_pincode = NULL) THEN
        SET NEW.order_billing_address_house_no = (SELECT customer_address_house_no FROM customer WHERE customer_ID = NEW.customer_ID);
        SET NEW.order_billing_address_city = (SELECT customer_address_city FROM customer WHERE customer_ID = NEW.customer_ID);
        SET NEW.order_billing_address_state = (SELECT customer_address_state FROM customer WHERE customer_ID = NEW.customer_ID);
        SET NEW.order_billing_address_pincode = (SELECT customer_address_pincode FROM customer WHERE customer_ID = NEW.customer_ID);
    END IF;
END;//


-- add a record into cart when a customer record is inserted, also set cart_Id = customer_ID
DROP TRIGGER IF EXISTS add_cart;
delimiter //
CREATE TRIGGER add_cart
AFTER INSERT ON customer
FOR EACH ROW
BEGIN
    INSERT INTO cart (cart_ID, customer_ID) VALUES (NEW.customer_ID, NEW.customer_ID);
END;//