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


# def search(product_name):
#     for product in product_dict.keys():
#         if str(product_name).lower() in product.lower():
#             return (f"{product_name} : ${product_dict[product_name]}")
#         else:
#             st.write(f"Sorry, {product_name} is not available.")


def customer_cart(customer_id):
    """display customer cart"""
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
        col1, col3, col4 = st.columns([2, 1, 1])
        with col1:
            st.write("Product Name")
        with col3:
            st.write("Price($)")
        with col4:
            st.write("Quantity")
        for result in results:
            with col1:
                st.write(result[0])
            with col3:
                st.write(result[2])
            with col4:
                new_qty = st.number_input("", value=result[1], step=1)
                if new_qty != result[1]:
                    query = """UPDATE Cart_contents SET product_quantity = %s 
                               WHERE cart_ID = 
                                    (SELECT cart_ID FROM Customer WHERE customer_ID = %s) 
                                    AND product_ID = %s"""
                    cursor.execute(query, (new_qty, customer_id, result[3]))
                    cnx.commit()
            total += result[1] * result[2]
        st.write(f"Total: {total:.2f}")


def customer_home(customer_id):
    """customer home page"""
    cursor.execute(f"SELECT cart_id FROM Customer WHERE customer_id = {customer_id};")
    cart_id = cursor.fetchone()[0]
    # st.form
    st.title("Home Page (Customer)")
    # search_term = st.text_input("Enter a product name:")
    # if st.button("Search"):
    #     for product in product_dict.values():
    #         if search_term.lower() in str(product[1]).lower():
    #             col1, col2, col3 = st.columns([2, 2, 1])
    #             col1.write(product[1])
    #             col2.write(f"Rs {product[2]:.2f}")
    #             if col3.button("Add to cart", key=product[0]):
    #                 query = f"INSERT INTO Cart_contents VALUES ({cart_id}, {product[0]}, 1);"
    #                 cursor.execute(query)
    #                 st.success(f"{product[1]} added to cart.")
    #         else:
    #             st.write(f"Sorry, {search_term} is not available.")
    # else:
    st.write(pd.DataFrame({
        'products': [product[1] for product in product_dict.values()],
        'price': [product[2] for product in product_dict.values()],
        'add to cart': [st.button(f"Add {product[1]}", key=product[0]) for product in product_dict.values()]
    }))

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
            st.success(msg)
            # write the code to navigate to customer home page
            customer_home(customer[0])
        else:
            st.error("Invalid email or password. Please try again.")

def admin_login():
    """admin login"""
    st.title("Admin Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login as Admin"):
        query = f"SELECT * FROM Admin WHERE admin_email={email} AND admin_password={password};"
        cursor.execute(query)
        admin = cursor.fetchone()
        if admin:
            query= f"Welcome back {admin[1]} {admin[2]}! (logged in as admin)"
            st.success(query)
        else:
            st.error("Invalid email or password.")

def main():
    st.set_page_config(page_title="Apni Dukan", page_icon=":moneybag:")
    menu = ["Customer Login", "Admin Login", "Customer Home", "Cart"]
    choice = st.sidebar.selectbox("Select a page", menu)

    if choice == "Admin Login":
        admin_login()
    
    elif choice == "Customer Login":
        customer_login()

    elif choice == "Cart":
        customer_cart(0)

    elif choice == "Customer Home":
        customer_home()

if __name__ == "__main__":
    main()

cursor.close()
cnx.close()