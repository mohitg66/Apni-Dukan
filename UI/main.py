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

# st.session_state["customer_id"] = None
# st.session_state["admin_id"] = None
    

def customer_cart():
    """display customer cart"""
    
    if 'customer_id' not in st.session_state or st.session_state['customer_id'] is None:
        st.info("Please login to view your cart.")
        return
    
    customer_id= st.session_state['customer_id']
    st.title("Your Cart")
    query = """SELECT Product.product_name, Cart_contents.product_quantity, Product.product_price, Cart_contents.product_ID
               FROM Cart_contents 
               INNER JOIN Product ON Cart_contents.product_ID = Product.product_ID 
               WHERE Cart_contents.cart_ID = 
                    (SELECT cart_ID FROM Customer WHERE customer_ID = %s)"""
    cursor.execute(query, (customer_id,))
    results = cursor.fetchall()
    if not results:
        st.write("Your cart is empty.")
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
        # if col1.button("Checkout", key="checkout"):
        #     st.success("Checkout successful!")
        if col2.button("Clear cart", key="clear"):
            query = """DELETE FROM Cart_contents 
                       WHERE cart_ID = 
                            (SELECT cart_ID FROM Customer WHERE customer_ID = %s)"""
            cursor.execute(query, (customer_id,))
            cnx.commit()
            st.success("Cart cleared!")
            st.experimental_rerun()

def admin_home():
    """admin home page"""
    
    if 'admin_id' not in st.session_state or st.session_state['admin_id'] is None:
        st.info("Please login to view this page.")
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
    
    

def customer_home():
    """customer home page"""
    # st.session_state
    if 'customer_id' not in st.session_state or st.session_state['customer_id'] is None:
        st.info("Please login to view the home page.")
        return
    
    cart_id= st.session_state['customer_id']
    
    st.title("Home Page (Customer)")
    
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
    search_term = col1.text_input("Enter a product name:", label_visibility="collapsed", placeholder="Search for a product")
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


# def customer_home(customer_id):
#     """customer home page"""
#     cursor.execute(f"SELECT cart_id FROM Customer WHERE customer_id = {customer_id};")
#     cart_id = cursor.fetchone()[0]
    
#     st.title("Home Page (Customer)")
    
#     # create a column layout for search bar and button
#     col1, col2 = st.columns([3, 1])
    
#     # create search bar in first column
#     search_term = col1.text_input("Enter a product name:")
    
#     # create search button in second column
#     search_button = col2.button("Search")
    
#     # create empty list to store products
#     products = []
    
#     # if search button is clicked, filter the products based on search term
#     if search_button:
#         for product in product_dict.values():
#             if search_term.lower() in str(product[1]).lower():
#                 products.append(product)
                
#         if not products:
#             st.write(f"Sorry, {search_term} is not available.")
    
#     # if search button is not clicked, show all the products
#     else:
#         products = list(product_dict.values())
    
#     # show the products
#     for product in products:
#         col1, col2, col3 = st.columns([2, 2, 1])
#         col1.write(product[1])
#         col2.write(f"Rs {product[2]:.2f}")
#         add_to_cart_button = col3.button("Add to cart", key=product[0])
        
#         # if add to cart button is clicked, insert the product into cart and show success message
#         if add_to_cart_button:
#             query = f"INSERT INTO Cart_contents VALUES ({cart_id}, {product[0]}, 1);"
#             cursor.execute(query)
#             st.success(f"{product[1]} added to cart.")



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
    menu = ["Customer Login", "Admin Login", "Admin Home", "Customer Home", "Cart"]
    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Admin Login":
        admin_login()
    
    elif choice == "Admin Home":
        admin_home()
    
    elif choice == "Customer Login":
        customer_login()

    elif choice == "Cart":
        customer_cart()

    elif choice == "Customer Home":
        customer_home()

if __name__ == "__main__":
    main()

# close the connection to the database
cursor.close()
cnx.commit()
