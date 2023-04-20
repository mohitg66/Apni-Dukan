### System Flow
Overall flow of the database system is as follows- there are a lot of customers in the database. There are many products in the database which are managed by admins. Each customer has a cart which can have some products or none. When a customer makes payment, an order is placed, and an order_id is generated. Then a delivery_ID is generated and a delivery is initiated for the order which is tracked by the system.

### ER model
<img src="ER diagram.svg" alt="ER diagram" width=""/>

### Relational Model
<img src="Relational model.svg" alt="ER diagram" width=""/>

### Database Schema
The file ‘ApniDukan-schema’ contains the sql code for the database schema. For creating the database schema, first, we drop the database (ApniDukan) if there exists any, and then we create a new database. Then we use the database, and create all the required relations in the database, following the relational model, along with the sufficient required constraints such as primary key and foreign key, using the CREATE command of sql.

### Data Population
The file ‘ApniDukan-data’ contains the sql code insertion of data into our database. For populating the database with data, we took help of an online bulk data generator, filldb, to get bulk random data according to all the relations and corresponding attributes. Then we inserted that data into the relations using INSERT command.