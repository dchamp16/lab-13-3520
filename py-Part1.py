import mysql.connector
from prettytable import PrettyTable

# Function to connect to the database using a context manager
def connect_to_database(user, passwd):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            passwd=passwd,
            database='lab13_db'
        )
        print(f"\n\nConnected to the database as {user}.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to insert a customer
def insert_customer(connection, employee_id, firstname, lastname, phone_number):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Customer (Employee_id, firstname, lastname, phone_number) VALUES (%s, %s, %s, %s)",
            (employee_id, firstname, lastname, phone_number)
        )
        connection.commit()
        print("Customer added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to update a customer's phone number
def update_customer(connection, employee_id, dataname, value):
    try:
        cursor = connection.cursor()
        # Using parameterized query for safety against SQL injection
        query = f"UPDATE Customer SET {dataname} = %s WHERE Employee_id = %s"
        cursor.execute(query, (value, employee_id))
        connection.commit()
        print(f"Customer's {dataname} updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Function to delete a customer
def delete_customer(connection, employee_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM Customer WHERE Employee_id = %s",
            (employee_id,)
        )
        connection.commit()
        print("Customer deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")



def list_customers(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Customer")

        # Fetch all rows and get column names
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        # Create a PrettyTable
        table = PrettyTable()
        table.field_names = columns

        # Add rows to the table
        for row in rows:
            table.add_row(row)

        # Print the table
        print(table)

    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Function to list all customers and their changes
def list_customers_with_changes(connection):
    try:
        cursor = connection.cursor()
        # Execute the SQL query
        cursor.execute("""
            SELECT c.*, ca.change_on
            FROM Customer c
            LEFT JOIN Customer_Audit ca ON c.Employee_id = ca.employee_id
        """)

        # Fetch all rows and get column names
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        # If the number of columns in the cursor description does not match the query, adjust accordingly
        # This is to ensure that the number of columns in PrettyTable matches the fetched data
        if len(columns) != len(rows[0]):
            columns.append("Last Change Timestamp")

        # Create a PrettyTable and set its field names
        table = PrettyTable()
        table.field_names = columns

        # Add rows to the table
        for row in rows:
            table.add_row(row)

        # Print the table
        print(table)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to delete all data from the Customer table
def delete_all_data_from_customer_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Customer")
        connection.commit()
        print("All data from the Customer table deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Checks if a customer with the specified employee_id already exists in the Customer table.
def customer_exists(connection, employee_id):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Customer WHERE Employee_id = %s",
            (employee_id,)
        )
        return cursor.fetchone()[0] > 0
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

# test users

# admin
def test_admin_user():
    user = 'admin'
    passwd = 'password'  # Replace with the actual password
    database_connection = connect_to_database(user, passwd)

    if database_connection:
        with database_connection as connection:
            print(f"Testing operations as {user}")

            if not customer_exists(connection, 11):
                try:
                    insert_customer(connection, 11, 'Test', 'Admin', '1111111111')
                except Exception as e:
                    print(f"Insert operation failed for admin user: {e}")
            else:
                print("Customer with Employee_id 11 already exists.")

            try:
                update_customer(connection, 11, 'firstname', 'AdminUpdated')
                list_customers(connection)
                delete_customer(connection, 11)
                print("All operations for admin user successful.")
            except Exception as e:
                print(f"Operation failed for admin user: {e}")

    else:
        print("Failed to connect to the database as admin.")


# sally
def test_sally_user():
    user = 'Sally'
    passwd = 'password'
    database_connection = connect_to_database(user, passwd)

    if database_connection:
        with database_connection as connection:
            print(f"\n\nTesting operations as {user}")

            try:
                list_customers(connection)
                print("SELECT operation successful for Sally.")
            except Exception as e:
                print(f"SELECT operation failed for Sally: {e}")

            # Attempt INSERT operation (expected to fail)
            try:
                insert_customer(connection, 12, 'Test', 'Sally', '2222222222')
                print("INSERT operation should have failed for Sally but succeeded.")
            except Exception as e:
                print("INSERT operation failed as expected for Sally:", e)

            # Attempt UPDATE operation (expected to fail)
            try:
                update_customer(connection, 1, 'firstname', 'SallyUpdated')
                print("UPDATE operation should have failed for Sally but succeeded.")
            except Exception as e:
                print("UPDATE operation failed as expected for Sally:", e)

            # Attempt DELETE operation (expected to fail)
            try:
                delete_customer(connection, 1)
                print("DELETE operation should have failed for Sally but succeeded.")
            except Exception as e:
                print("DELETE operation failed as expected for Sally:", e)

    else:
        print("Failed to connect to the database as Sally.")

# tom

def test_tom_user():
    user = 'Tom'
    passwd = 'password'
    database_connection = connect_to_database(user, passwd)

    if database_connection:
        with database_connection as connection:
            print(f"\n\nTesting operations as {user}")

            if not customer_exists(connection, 13):
                try:
                    insert_customer(connection, 13, 'Test', 'Tom', '3333333333')
                except Exception as e:
                    print(f"Insert operation failed for Tom: {e}")
            else:
                print("Customer with Employee_id 13 already exists.")

            try:
                update_customer(connection, 13, 'firstname', 'TomUpdated')
                list_customers(connection)
                print("INSERT and UPDATE operations successful for Tom.")
            except Exception as e:
                print(f"Operation failed for Tom: {e}")

            # Attempt DELETE operation (expected to fail)
            try:
                delete_customer(connection, 13)
                print("DELETE operation should have failed for Tom but succeeded.")
            except Exception as e:
                print("DELETE operation failed as expected for Tom:", e)

    else:
        print("Failed to connect to the database as Tom.")


# Sample data: Array of 10 employees with unique Employee_id
employees = [
    {
        "employee_id": 1,
        "firstname": "Alice",
        "lastname": "Wonderland",
        "phone_number": "555-123-4567"
    },
    {
        "employee_id": 2,
        "firstname": "Bob",
        "lastname": "Unicorn",
        "phone_number": "555-987-6543"
    },
    {
        "employee_id": 3,
        "firstname": "Charlie",
        "lastname": "Dragon",
        "phone_number": "555-789-0123"
    },
    {
        "employee_id": 4,
        "firstname": "Daisy",
        "lastname": "Mermaid",
        "phone_number": "555-456-7890"
    },
    {
        "employee_id": 5,
        "firstname": "Eva",
        "lastname": "Phoenix",
        "phone_number": "555-876-5432"
    },
    {
        "employee_id": 6,
        "firstname": "Felix",
        "lastname": "Yeti",
        "phone_number": "555-234-5678"
    },
    {
        "employee_id": 7,
        "firstname": "Grace",
        "lastname": "Sasquatch",
        "phone_number": "555-345-6789"
    },
    {
        "employee_id": 8,
        "firstname": "Hugo",
        "lastname": "Mothman",
        "phone_number": "555-789-1234"
    },
    {
        "employee_id": 9,
        "firstname": "Ivy",
        "lastname": "Kraken",
        "phone_number": "555-654-3210"
    },
    {
        "employee_id": 10,
        "firstname": "Jack",
        "lastname": "Chimera",
        "phone_number": "555-432-1098"
    }
]

test_admin_user()
test_sally_user()
test_tom_user()

# Test if the program can connect to the database
user = 'admin'  # Replace with your actual MySQL username
passwd = 'password'  # Replace with your actual MySQL password
database_connection = connect_to_database(user, passwd)
if database_connection:
    with database_connection as connection:
        print(f"Logged in as {user}")

        # Insert each employee from the array into the database only if they don't already exist
        # for employee in employees:
        #     if not customer_exists(connection, employee["employee_id"]):
        #         insert_customer(
        #             connection,
        #             employee["employee_id"],
        #             employee["firstname"],
        #             employee["lastname"],
        #             employee["phone_number"]
        #         )
        #     else:
        #         print(f"Customer with Employee_id {employee['employee_id']} already exists.")

        list_customers_with_changes(connection)

else:
    print("Failed to connect to the database.")

