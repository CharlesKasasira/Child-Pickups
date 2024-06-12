import psycopg2

# Database connection parameters
connection = psycopg2.connect(
    host="aws-0-us-east-1.pooler.supabase.com",
    port="5432",
    user="postgres.hmztmelqhqsooxziulqd",
    password="dbpassword#2024#childPickUp",
    database="postgres"
)

cursor = connection.cursor()

# SQL command to add the email column
add_column_sql = """
ALTER TABLE children_management_driver ADD COLUMN email VARCHAR(100) UNIQUE;
"""

try:
    # Execute the SQL command
    cursor.execute(add_column_sql)
    # Commit the changes
    connection.commit()
    print("Email column added successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
    connection.rollback()
finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
