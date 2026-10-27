
import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=ISMAIL\SQLEXPRESS;"
    "DATABASE=olistDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    connection = pyodbc.connect(connection_string, timeout=10)
    cursor = connection.cursor()

    cursor.execute("SELECT DB_NAME()")
    print("Connected successfully!")
    print("Database:", cursor.fetchone()[0])

    cursor.close()
    connection.close()

except pyodbc.Error as error:
    print("Connection failed:")
    print(error)


olist_customers_dataset.describe()