# Apni Dukan
Apni Dukan is an online e-commerce retail store where users can browse and purchase products from various categories such as electronics, clothing, and household items. This project was developed as part of a DBMS course.

## Tech Stack
<img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" height="60px" /> <img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" height="60px"> <img src="https://seeklogo.com/images/S/streamlit-logo-1A3B208AE4-seeklogo.com.png" height="60px">

## Features
- **User authentication**: Users can create an account and log in to access the site's features
- **Admin functionalities**: Admins can create an account and log in to access the site's admin features
- **Product browsing**: Users can browse products by category or search for specific items using keywords
- **Cart management**: Users can add items to their shopping cart, view their cart, and remove items from their cart
- **Checkout**: Users can complete their purchase by entering their shipping and billing information
- **Order history**: Users can view their past orders and track their current order status

## ER model
<img src="ER diagram.svg" alt="ER diagram" width=""/>

## Relational Model
<img src="Relational model.svg" alt="ER diagram" width=""/>

## Instructions
- Clone the repository

    ```
    git clone https://github.com/mohitg66/Apni-Dukan.git
    cd apni-dukan
    ```
- Install MySQL if not installed already
- Import the database using the SQL scripts in root directory
- Install dependencies    
    ``` 
    pip install streamlit
    ```
- Run the app
    ```
    cd UI
    streamlit run main.py
    ```
- Navigate to http://localhost:8501 in your web browser to access the site


## Authors
- **Mohit Gupta**
- **Kartikye Prasad**