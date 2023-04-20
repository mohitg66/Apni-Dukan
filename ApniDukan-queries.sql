
-- Display the products that are out of stock
SELECT product_ID, product_name
FROM Product
WHERE product_available_quantity = 0;

-- Display all customers who have made a purchase from the "nemo" category    
SELECT 
    customer_ID, customer_fname
FROM
    Customer
        INNER JOIN
    Payment using(customer_ID)
        INNER JOIN
    Order_contents USING (order_ID)
        INNER JOIN
    Product USING (product_ID)
        INNER JOIN
    category USING (category_ID)
WHERE
    category_name = 'nemo';

-- Update the price of all products in the "nemo" category to decrease by 10%
UPDATE Product
SET product_price = product_price * 0.9
WHERE category_ID IN (
    SELECT category_ID
    FROM Category
    WHERE category_name = 'nemo'
);

-- Display all available products from the 'nemo' category along with their prices
SELECT 
    Product.product_name, Product.product_price
FROM
    (Product
    INNER JOIN Category ON Product.category_ID = Category.category_ID)
WHERE
    Product.product_available_quantity > 0
        AND Category.category_name = 'nemo';

-- Display all the admins with the number of products managed by each of them
SELECT 
    admin_ID, admin_fname, COUNT(product_ID)
FROM
    (Admin
    INNER JOIN Product USING (admin_ID))
GROUP BY admin_ID;

-- Delete all the customers who haven't placed any order yet
SET sql_safe_updates= 0;
DELETE FROM Customer 
WHERE
    customer_ID 
    NOT IN (SELECT DISTINCT customer_ID FROM Payment);
SET sql_safe_updates= 1;

-- Insert a new product into the "nemo" category
INSERT INTO Product
VALUES (
	1002,
    'Apple Watch Series 6',
    420,
    'A healthy leap ahead...',
    'Apple',
    'https://loremflickr.com/640/48',
    4.6,
    200, 
    572,
    (SELECT category_ID FROM Category WHERE category_name = 'nemo')
);

-- Display the product_ID, product_name of all the products present in the cart of those customers whose age is less than 18
  SELECT 
    product_ID, product_name, customer_dob
FROM
    ((Customer
    INNER JOIN cart_contents USING (cart_ID))
    INNER JOIN product USING (product_ID))
WHERE
    year(customer_dob) > year(curdate())-18;
    
-- Display the number of products with rating more than 4 in each category
SELECT 
    category_name, COUNT(product_ID)
FROM
    (Category
    INNER JOIN Product USING (category_ID))
WHERE
    product_rating > 4
GROUP BY category_ID;

-- Display the customer_ID and names of the customers who have made any order in the year 2023
SELECT 
    customer_ID, customer_fname
FROM
    (Payment
    INNER JOIN customer USING (customer_ID))
WHERE
    YEAR(payment_date) = 2023;

-- Display the order_ID of the deliveries which are pending or not initiated
SELECT 
    order_ID
FROM
    (Orders
    LEFT JOIN Delivery USING (order_ID))
WHERE
    delivery_status LIKE 'pend%' OR delivery_status IS NULL;

-- Replace a customer's details
REPLACE INTO Customer 
VALUES (
    55,
    'Shaurya',
    'Singh',
    'soorya420@manipal.com',
    'password123',
    '2000-01-26',
    'B-2/82',
    'New Delhi',
    'Delhi',
    '110023',
    1
);