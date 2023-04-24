import random
import time
import streamlit as st
import pandas as pd
import mysql.connector

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mohitbhai",
    database="apnidukan"
)

cursor = cnx.cursor()
cursor.execute("SELECT * FROM Product")
rows = cursor.fetchall()
product_dict = {}
for row in rows:
    product_dict[row[0]]= row

    
def customer_orders():
    """Display customer's previous orders"""
    st.title("Order History")
    if 'customer_id' not in st.session_state or st.session_state['customer_id'] is None:
        st.warning("Please login to view your order history.")
        return
    
    # if 'order_id' not in st.session_state or st.session_state['order_id'] is None:
    #     st.info("You do not have any previous orders.")
    #     return
    
    customer_id= st.session_state['customer_id']
    # order_id= st.session_state['order_id']
    query = f"SELECT O.order_ID, O.order_amount, O.order_date, O.order_status FROM Orders O INNER JOIN Order_contents OC ON O.order_ID = OC.order_ID INNER JOIN Payment P ON O.order_ID=P.order_ID WHERE P.customer_ID = {customer_id}"
    cursor.execute(query)
    orders = cursor.fetchall()
    
    if not orders:
        st.info("You do not have any previous orders.")
        return
    
    query = f"SELECT customer_fname, customer_lname FROM Customer WHERE customer_ID = {customer_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    customer_fname, customer_lname = result
    st.write(f"Previous orders of {customer_fname} {customer_lname}:")
    
    column_widths = [max(len(str(order[i])) for order in orders) for i in range(4)]        
    column_widths = [width + 3 for width in column_widths]        
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("<h5>Order ID</h5>", unsafe_allow_html=True)
    col2.markdown("<h5>Order Amount</h5>", unsafe_allow_html=True)
    col3.markdown("<h5>Order Date</h5>", unsafe_allow_html=True)
    col4.markdown("<h5>Order Status</h5>", unsafe_allow_html=True)
    for order in orders:
        col1, col2, col3, col4 = st.columns(4)
        col1.write('#'+str(order[0]), justify="center", width=column_widths[0])
        col2.write(str(order[1]), justify="center", width=column_widths[1])
        col3.write(str(order[2]), justify="center", width=column_widths[2])
        col4.write(str(order[3]), justify="center", width=column_widths[3])


def customer_cart():
    """display customer cart"""
    st.title("Your Cart")
    
    if 'customer_id' not in st.session_state or st.session_state['customer_id'] is None:
        st.warning("Please login to view your cart.")
        return
    customer_id= st.session_state['customer_id']
    
    query = f"SELECT customer_fname, customer_lname FROM Customer WHERE customer_ID = {customer_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    customer_fname, customer_lname = result
    st.write(f"Cart of {customer_fname} {customer_lname}:")
    
    query = """SELECT Product.product_name, Cart_contents.product_quantity, Product.product_price, Cart_contents.product_ID
               FROM Cart_contents 
               INNER JOIN Product ON Cart_contents.product_ID = Product.product_ID 
               WHERE Cart_contents.cart_ID = 
                    (SELECT cart_ID FROM Customer WHERE customer_ID = %s)"""
    cursor.execute(query, (customer_id,))
    results = cursor.fetchall()
    
    if not results:
        st.info("Your cart is empty.")
    else:
        total = 0
        st.divider()
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1: st.subheader("Product")
        with col2: st.subheader("Price")
        with col3: st.subheader("Quantity")
        st.divider()
        for result in results:
            col1, col2, col3 = st.columns([4, 1, 1])
            st.divider()
            col1.write(result[0])
            col2.write(f"Rs {result[2]:.2f}")
            new_qty = col3.number_input("Quantity", value=result[1], step=1, min_value=0, key=result[3], label_visibility="collapsed")
            if new_qty != result[1]:
                query = """UPDATE Cart_contents SET product_quantity = %s 
                           WHERE cart_ID = 
                                (SELECT cart_ID FROM Customer WHERE customer_ID = %s) 
                                AND product_ID = %s"""
                cursor.execute(query, (new_qty, customer_id, result[3]))
                cnx.commit()
            total += new_qty * result[2]
            
        col1, col2 = st.columns([4, 2])
        col1.subheader("Total")
        col2.subheader(f"Rs {total:.2f}")
        st.divider()
        
        col1, col2 = st.columns([5, 1])
        if col1.button("Checkout", key="checkout"):
            order_id= random.randint(100000, 999999)
            
            query= "SELECT order_ID FROM Orders"
            cursor.execute(query)
            results = cursor.fetchall()
            while order_id in results:
                order_id= random.randint(100000, 999999)
                cursor.execute(query)
                results = cursor.fetchall()
            
            query= f"INSERT INTO Orders (order_ID, order_amount, order_date, order_status) VALUES ({order_id}, {total}, CURDATE(), 'Pending');"
            cursor.execute(query)
            st.session_state['order_id']= order_id
                        
            query= f"INSERT INTO Order_contents (order_ID, product_ID, product_quantity) SELECT {order_id}, product_ID, product_quantity FROM Cart_contents WHERE cart_ID = {customer_id};"
            cursor.execute(query)
            
            payment_id= random.randint(100000, 999999)
            query= "SELECT payment_ID FROM Payment"
            cursor.execute(query)
            results = cursor.fetchall()
            while payment_id in results:
                payment_id= random.randint(100000, 999999)
                cursor.execute(query)
                results = cursor.fetchall()
            
            query= f"INSERT INTO Payment (order_ID, customer_ID, payment_ID, payment_amount, payment_date, payment_status) VALUES ({order_id}, {customer_id}, {payment_id}, {total}, CURDATE(), 'Completed');"
            cursor.execute(query)
                                   
            query = f"DELETE FROM Cart_contents WHERE cart_ID = (SELECT cart_ID FROM Customer WHERE customer_ID = {customer_id})"
            cursor.execute(query)

            st.success("Checkout successful!")
            cnx.commit()
            
        elif col2.button("Clear cart", key="clear"):
            query = """DELETE FROM Cart_contents 
                       WHERE cart_ID = 
                            (SELECT cart_ID FROM Customer WHERE customer_ID = %s)"""
            cursor.execute(query, (customer_id,))
            cnx.commit()
            st.success("Cart cleared!")
            st.experimental_rerun()


def customer_home():
    """customer home page"""
    
    st.title("Home Page (Customer)")
    
    if 'customer_id' not in st.session_state or st.session_state['customer_id'] is None:
        st.warning("Please login to view the home page.")
        return
    
    cart_id= st.session_state['customer_id']
    
    query= f"SELECT customer_fname, customer_lname FROM Customer WHERE customer_ID = {st.session_state['customer_id']};"
    cursor.execute(query)
    results = cursor.fetchone()
    
    st.write(f"Welcome, {results[0]} {results[1]}!")
    
    # Get the current contents of the cart
    query= f"SELECT product_id, product_quantity FROM Cart_contents WHERE cart_id = {cart_id};"
    cursor.execute(query)
    cart_contents = cursor.fetchall()
    if cart_contents:
        cart_dict = {product[0]: product[1] for product in cart_contents}
    else:
        cart_dict = {}
        
    
    # search bar and button
    products = []
    col1, col2 = st.columns([5, 1], gap="large")
    search_term = col1.text_input("Enter a product name:", label_visibility="collapsed", placeholder="Search for a product", key="search_term")
    if col2.button("Search"):
        products = []
        for product in product_dict.values():
            if search_term.lower() in str(product[1]).lower():
                products.append(product)
    else:
        for product in product_dict.values():
            products.append(product)
            
    # Display the products
    st.divider()
    if not products:
        st.error("No products found")
    else:
        for product in products:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            col1.write(product[1])
            col2.write(f"Rs {product[2]:.2f}")

            # Display the quantity input and "Add to cart" button
            quantity = col3.number_input("Quantity", min_value=0, value=0, step=1, key=f"quantity_{product[0]}", label_visibility="collapsed")
            if col4.button("Add to cart", key=f"add_{product[0]}"):
                # If the "Add to cart" button is clicked, update the cart in the database
                if cart_dict and product[0] in cart_dict:
                    new_quantity = cart_dict[product[0]] + quantity
                    query = f"UPDATE Cart_contents SET product_quantity = {new_quantity} WHERE cart_id = {cart_id} AND product_id = {product[0]};"
                else:
                    query = f"INSERT INTO Cart_contents VALUES ({cart_id}, {product[0]}, {quantity});"
                    cursor.execute(query)
                    cart_dict[product[0]] = quantity
                    cnx.commit()
                st.success(f"{quantity} {product[1]} added to cart.")
            st.divider()


def customer_login():
    """customer login"""
    st.title("Customer Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login as customer"):
        query = f"SELECT * FROM Customer WHERE customer_email = '{email}' AND customer_password = '{password}';"
        cursor.execute(query)
        customer = cursor.fetchone()
        if customer:
            msg = f"Welcome back {customer[1]} {customer[2]}! (logged in as customer)"
            # call the customer_home function with the customer_id and product_dict parameters
            st.session_state["customer_id"] = customer[0]
            query= f"INSERT IGNORE INTO Cart (cart_id, cart_amount) VALUES ({customer[0]}, 0);"
            cursor.execute(query)
            query= f"UPDATE Customer SET cart_id = {customer[0]} WHERE customer_id = {customer[0]};"
            cursor.execute(query)
            cnx.commit()
            st.success(msg)
        else:
            st.error("Invalid email or password. Please try again.")


def customer_signup():
    """customer signup"""
    st.title("Customer Signup")
    
    customer_id = random.randint(100000, 999999)
    query = "SELECT customer_ID FROM Customer"
    cursor.execute(query)
    results = cursor.fetchall()
    while customer_id in results:
        customer_id = random.randint(100000, 999999)
        cursor.execute(query)
        results = cursor.fetchall()
    
    col1, col2 = st.columns(2)
    with col1:
        customer_fname = st.text_input("First Name")
    with col2:
        customer_lname = st.text_input("Last Name")
    customer_email = st.text_input("Email")
    customer_password = st.text_input("Password", type="password")
    customer_dob = st.date_input("Date of Birth")
    customer_address_house_no = st.text_input("House Number")
    customer_address_city = st.text_input("City")
    customer_address_state = st.text_input("State")
    customer_address_pincode = st.text_input("Pincode")

    if st.button("Sign Up"):
        query = f"INSERT INTO Customer (customer_ID, customer_fname, customer_lname, customer_email, customer_password, customer_dob, customer_address_house_no, customer_address_city, customer_address_state, customer_address_pincode) VALUES ({customer_id}, '{customer_fname}', '{customer_lname}', '{customer_email}', '{customer_password}', '{customer_dob}', '{customer_address_house_no}', '{customer_address_city}', '{customer_address_state}', '{customer_address_pincode}');"
        try:
            cursor.execute(query)
            cnx.commit()
            st.session_state["customer_id"] = customer_id
            st.success(f"Signed up as customer successfully! Welcome {customer_fname} {customer_lname}!")
        except mysql.connector.IntegrityError as id_duplicate_error:
            st.error("ID already exists. Please try again with a different ID.")


def admin_home():
    """admin home page"""
    if 'admin_id' not in st.session_state or st.session_state['admin_id'] is None:
        st.warning("Please login to view this page.")
        return
    
    st.title("Home Page (Admin)")
    st.divider()
    N= 11
    queries= [[None for i in range(2)] for j in range(N)]
    queries[0][0]= "Display the products that are out of stock"
    queries[0][1]= """
        SELECT product_ID, product_name
        FROM Product
        WHERE product_available_quantity = 0;"""
    queries[1][0]= "Display all customers who have made a purchase from the 'Electronics' category"
    queries[1][1]= """
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
            category_name = 'Electronics';"""
            
    queries[2][0]= "Update the price of all products in the 'Electronics' category to decrease by 10%"
    queries[2][1]= """
        UPDATE Product
        SET product_price = product_price * 0.9
        WHERE category_ID IN (
            SELECT category_ID
            FROM Category
            WHERE category_name = 'Electronics'
        );"""
        
    queries[3][0]= "Display all available products from the 'Electronics' category along with their prices"
    queries[3][1]= """
    SELECT 
        Product.product_name, Product.product_price
    FROM
        (Product
        INNER JOIN Category ON Product.category_ID = Category.category_ID)
    WHERE
        Product.product_available_quantity > 0
            AND Category.category_name = 'Electronics';"""
            
    queries[4][0]= "Display all the admins with the number of products managed by each of them"
    queries[4][1]= """
    SELECT 
        admin_ID, admin_fname, COUNT(product_ID)
    FROM
        (Admin
        INNER JOIN Product USING (admin_ID))
    GROUP BY admin_ID;"""
    
    queries[5][0]= "Delete all the customers who haven't placed any order yet"
    queries[5][1]= """
    SET sql_safe_updates= 0;
    DELETE FROM Customer 
    WHERE
        customer_ID 
        NOT IN (SELECT DISTINCT customer_ID FROM Payment);
    SET sql_safe_updates= 1;
    """
    
    queries[6][0]= "Insert a new product into the 'Electronics' category"
    queries[6][1]= """
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
        (SELECT category_ID FROM Category WHERE category_name = 'Electronics')
    );"""
    
    queries[7][0]= "Display the product_ID, product_name of all the products present in the cart of those customers whose age is less than 18"
    queries[7][1]= """
    SELECT 
        product_ID, product_name, customer_dob
    FROM
        ((Customer
        INNER JOIN cart_contents USING (cart_ID))
        INNER JOIN product USING (product_ID))
    WHERE
        year(customer_dob) > year(curdate())-18;"""
    
    queries[8][0]= "Display the number of products with rating more than 4 in each category"
    queries[8][1]= """
    SELECT 
        category_name, COUNT(product_ID)
    FROM
        (Category
        INNER JOIN Product USING (category_ID))
    WHERE
        product_rating > 4
    GROUP BY category_ID;"""
    
    queries[8][0]= "Display the customer_ID and names of the customers who have made any order in the year 2023"
    queries[8][1]= """
    SELECT 
        customer_ID, customer_fname
    FROM
        (Payment
        INNER JOIN customer USING (customer_ID))
    WHERE
        YEAR(payment_date) = 2023;"""
        
    queries[9][0]= "Display the order_ID of the deliveries which are pending or not initiated"
    queries[9][1]= """
    SELECT 
        order_ID
    FROM
        (Orders
        LEFT JOIN Delivery USING (order_ID))
    WHERE
        delivery_status LIKE 'pend%' OR delivery_status IS NULL;"""
        
    queries[10][0]= "Replace a customer's details"
    queries[10][1]= """
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
    );"""
    
          
    for i in range(0,N):
        col1, col2, col3= st.columns([1, 5,1])
        col1.write(str(i+1))
        with col2:
            st.write(queries[i][0]) 
        with col3:
            if st.button("Run", key=f"run{i}"):
                cursor.execute(queries[i][1])
                results = cursor.fetchall()
                with col1: st.table(results)
                cnx.commit()
        st.divider()    


def admin_login():
    """admin login"""
    st.title("Admin Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login as Admin"):
        query = f"SELECT * FROM Admin WHERE admin_email='{email}' AND admin_password='{password}';"
        cursor.execute(query)
        admin = cursor.fetchone()
        if admin:
            st.session_state["admin_id"] = admin[0]
            st.success(f"Welcome back {admin[1]} {admin[2]}! (logged in as admin)")
        else:
            st.error("Invalid email or password.")

def main():
    st.set_page_config(page_title="Apni Dukan", page_icon=":moneybag:")
    menu = ["Customer Login", "Customer Signup" , "Admin Login", "Admin Home", "Customer Home", "Cart", "Orders"]
    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Admin Login":
        admin_login()
    
    elif choice == "Admin Home":
        admin_home()
    
    elif choice == "Customer Signup":
        customer_signup()
    
    elif choice == "Customer Login":
        customer_login()
        
    elif choice == "Customer Sign Up":
        customer_signup()

    elif choice == "Customer Home":
        customer_home()
        
    elif choice == "Cart":
        customer_cart()
    
    elif choice == "Orders":
        customer_orders()

if __name__ == "__main__":
    main()

# close the connection to the database
cursor.close()
cnx.commit()
