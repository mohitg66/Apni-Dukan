### System Flow
Overall flow of the database system is as follows- there are a lot of customers in the database. There are many products in the database which are managed by admins. Each customer has a cart which can have some products or none. When a customer makes payment, an order is placed, and an order_id is generated. Then a delivery_ID is generated and a delivery is initiated for the order which is tracked by the system.

### ER model
[link](https://lucid.app/lucidchart/3003addf-ef66-49bc-89ba-ba500bd99d54/edit?viewport_loc=700%2C574%2C3162%2C1481%2CUYHv-xkk2Qg6&invitationId=inv_f8dbf540-8583-4675-a851-8ee72b7922ee)

### Relational Model
[link](https://lucid.app/lucidchart/3003addf-ef66-49bc-89ba-ba500bd99d54/edit?viewport_loc=700%2C574%2C3162%2C1481%2CUYHv-xkk2Qg6&invitationId=inv_f8dbf540-8583-4675-a851-8ee72b7922ee)

### Database Schema
The file ‘ApniDukan-schema’ contains the sql code for the database schema. For creating the database schema, first, we drop the database (ApniDukan) if there exists any, and then we create a new database. Then we use the database, and create all the required relations in the database, following the relational model, along with the sufficient required constraints such as primary key and foreign key, using the CREATE command of sql.

### Data Population
The file ‘ApniDukan-data’ contains the sql code insertion of data into our database. For populating the database with data, we took help of an online bulk data generator, filldb, to get bulk random data according to all the relations and corresponding attributes. Then we inserted that data into the relations using INSERT command.