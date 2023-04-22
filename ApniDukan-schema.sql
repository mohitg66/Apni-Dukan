DROP DATABASE IF EXISTS ApniDukan;
CREATE DATABASE ApniDukan;
USE ApniDukan;

CREATE TABLE Admin (
    admin_ID INT,
    admin_fname VARCHAR(30),
    admin_lname VARCHAR(30),
    admin_email VARCHAR(30),
    admin_password VARCHAR(30),
    PRIMARY KEY (admin_ID)
);

CREATE TABLE Category (
    category_ID INT,
    category_name VARCHAR(30),
    PRIMARY KEY (category_ID)
);

CREATE TABLE Product (
    product_ID INT,
    product_name VARCHAR(50),
    product_price FLOAT,
    product_description VARCHAR(100),
    product_brand VARCHAR(30),
    product_image VARCHAR(50),
    product_rating FLOAT,
    product_available_quantity INT,
    admin_ID INT,
    category_ID INT,
    PRIMARY KEY (product_ID),
    FOREIGN KEY (admin_ID)
        REFERENCES Admin (admin_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (category_ID)
        REFERENCES Category (category_ID)
        ON DELETE SET NULL,
    CONSTRAINT rating_check CHECK (product_rating <= 5)
);

CREATE TABLE Cart (
    cart_ID INT,
    cart_amount FLOAT,
    PRIMARY KEY (cart_ID)
);

CREATE TABLE Cart_contents (
    cart_ID INT,
    product_ID INT,
    product_quantity INT,
    PRIMARY KEY (cart_ID , product_ID),
    FOREIGN KEY (cart_ID)
        REFERENCES Cart (cart_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (product_ID)
        REFERENCES Product (product_ID)
        ON DELETE CASCADE
    -- UNIQUE INDEX unique_carts (cart_ID)
);

CREATE TABLE Customer (
    customer_ID INT,
    customer_fname VARCHAR(30),
    customer_lname VARCHAR(30),
    customer_email VARCHAR(30),
    customer_password VARCHAR(30),
    customer_balance INT,
    customer_dob DATE,
    customer_address_house_no VARCHAR(30),
    customer_address_city VARCHAR(30),
    customer_address_state VARCHAR(30),
    customer_address_pincode VARCHAR(6),
    cart_ID INT,
    PRIMARY KEY (customer_ID),
    FOREIGN KEY (cart_ID)
        REFERENCES Cart (cart_ID)
        ON DELETE SET NULL
);

CREATE TABLE Customer_phone (
    customer_ID INT,
    customer_phone VARCHAR(13),
    PRIMARY KEY (customer_ID , customer_phone),
    FOREIGN KEY (customer_ID)
        REFERENCES Customer (customer_ID)
        ON DELETE CASCADE
);

CREATE TABLE Orders (
    order_ID INT,
    order_amount FLOAT,
    order_date DATE,
    order_status VARCHAR(30),
    order_billing_address_house_no VARCHAR(30),
    order_billing_address_city VARCHAR(30),
    order_billing_address_state VARCHAR(30),
    order_billing_address_pincode VARCHAR(6),
    PRIMARY KEY (order_ID)
);

CREATE TABLE Order_contents (
    order_ID INT,
    product_ID INT,
    product_quantity INT,
    PRIMARY KEY (order_ID , product_ID),
    FOREIGN KEY (order_ID)
        REFERENCES Orders (order_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (product_ID)
        REFERENCES Product (product_ID)
        ON DELETE CASCADE
);

CREATE TABLE Payment (
    order_ID INT,
    customer_ID INT NOT NULL,
    payment_ID INT,
    payment_amount FLOAT,
    payment_date DATE,
    payment_status VARCHAR(30),
    PRIMARY KEY (order_ID),
    FOREIGN KEY (order_ID)
        REFERENCES Orders (order_ID)
        ON DELETE CASCADE,
    FOREIGN KEY (customer_ID)
        REFERENCES Customer (customer_ID)
        ON DELETE CASCADE
);

CREATE TABLE Delivery (
    delivery_ID INT,
    delivery_date DATE,
    delivery_status VARCHAR(30),
    delivery_address_house_no VARCHAR(30),
    delivery_address_city VARCHAR(30),
    delivery_address_state VARCHAR(30),
    delivery_address_pincode VARCHAR(6),
    order_ID INT,
    PRIMARY KEY (delivery_ID),
    FOREIGN KEY (order_ID)
        REFERENCES Orders (order_ID)
        ON DELETE CASCADE
    -- UNIQUE INDEX unique_orders (order_ID)
);

