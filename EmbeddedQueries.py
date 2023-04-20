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

def execute(query):
    
    # try catch block
    try:
        myCursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        print("\nInvalid query!")
        return
    
    myResult= myCursor.fetchall()
    

    table= Table(show_header= True, header_style= "bold blue")
    for x in myCursor.description:
        table.add_column(x[0], style= "blue", width= 20)

    for x in myResult:
        table.add_row(*[str(i) for i in x])
    
    console= Console()
    console.print(table)

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
menuTable= Table(show_header= True, header_style= "bold white")
menuTable.add_column("Query Number", style= "white", width= 20)
menuTable.add_column("Query", style= "white", width= 100)

menuTable.add_row("1", "Display the number of products with rating more than 4 in each category")
menuTable.add_row("2", "Display all the products with rating 5")
menuTable.add_row("3", "Custom Query")
menuTable.add_row("4", "Exit")

console= Console()
console.print(menuTable)


choice= int(input("Enter your choice: "))
while(choice!=4):
    print()
    
    if (choice == 1):
        execute(query1)
        
    elif (choice == 2):
        execute(query2)
            
    elif (choice == 3):
        query= input("Enter your query: ")
        execute(query)
                        
    elif (choice == 4):
        break
    
    else:
        print("Invalid choice!")
    
    print()
    print()
    choice= int(input("Enter your choice: "))

