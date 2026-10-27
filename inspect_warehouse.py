
import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=ISMAIL\SQLEXPRESS;"
    "DATABASE=olistDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

cursor.execute("""
    SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'GOLD'
    ORDER BY TABLE_NAME, ORDINAL_POSITION;
""")

rows = cursor.fetchall()
current_object = None

for row in rows:
    object_name = f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}"

    if object_name != current_object:
        print(f"\n{object_name}")
        current_object = object_name

    print(f"  - {row.COLUMN_NAME} ({row.DATA_TYPE})")

cursor.close()
connection.close()
