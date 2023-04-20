from rich.console import Console
from rich.table import Table
import mysql.connector

db= mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "Mohitbhai",
    database= "ApniDukan"
)

myCursor= db.cursor()
queries= []

def execute(i):
    myCursor.execute(queries[i])
    myResult= myCursor.fetchall()
    table= Table(show_header= True, header_style= "bold")
    table.add_column("Category Name", style= "white", width= 20)
    table.add_column("Number of Products", style= "white", width= 20)

    for x in myResult:
        table.add_row(str(x[0]), str(x[1]))
    

# Display the number of products with rating more than 4 in each category
query1= """
    SELECT 
        category_name, COUNT(product_ID)
    FROM
        (Category
        INNER JOIN Product USING (category_ID))
    WHERE
        product_rating > 4
    GROUP BY category_ID;"""
    
# Display all the products with rating 5
query2= """
    SELECT 
        product_ID, product_name, product_price, product_rating, category_ID
    FROM
        product
    WHERE
        product_rating = 5;"""
    
    
print()
menuTable= Table(show_header= True, header_style= "bold blue")
menuTable.add_column("Query Number", style= "blue", width= 20)
menuTable.add_column("Query", style= "blue", width= 100)

menuTable.add_row("1", "Display the number of products with rating more than 4 in each category")
menuTable.add_row("2", "Display all the products with rating 5")

console= Console()
console.print(menuTable)

choice= int(input("Enter your choice: "))
print()


if (choice == 1):
    myCursor.execute(query1)
    myResult= myCursor.fetchall()

    table= Table(show_header= True, header_style= "bold")
    table.add_column("Category Name", style= "white", width= 20)
    table.add_column("Number of Products", style= "white", width= 20)

    for x in myResult:  
        table.add_row(str(x[0]), str(x[1]))

else:
    myCursor.execute(query2)
    myResult= myCursor.fetchall()
    
    table= Table(show_header= True, header_style= "bold")
    table.add_column("Product ID", style= "white", width= 20)
    table.add_column("Product Name", style= "white", width= 20)
    table.add_column("Product Price", style= "white", width= 20)
    table.add_column("Product Rating", style= "white", width= 20)
    table.add_column("Category ID", style= "white", width= 20)

    for x in myResult:
        table.add_row(str(x[0]), str(x[1]), str(x[2]), str(x[3]), str(x[4]))
    

console.print(table)

