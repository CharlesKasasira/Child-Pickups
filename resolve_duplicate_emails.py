import psycopg2

# Database connection parameters
DB_NAME = 'postgres'
DB_USER = 'postgres.hmztmelqhqsooxziulqd'
DB_PASSWORD = 'dbpassword#2024#childPickUp'
DB_HOST = 'aws-0-us-east-1.pooler.supabase.com'
DB_PORT = '5432'

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        # Create a cursor object
        cur = conn.cursor()
        
        # Find duplicate emails
        cur.execute("""
            SELECT email, COUNT(*) 
            FROM children_management_driver
            GROUP BY email
            HAVING COUNT(*) > 1;
        """)
        duplicates = cur.fetchall()

        if not duplicates:
            print("No duplicate emails found.")
        else:
            print("Duplicate emails found. Resolving duplicates...")

            # Update duplicate emails to unique values
            for email, count in duplicates:
                cur.execute("""
                    SELECT id 
                    FROM children_management_driver 
                    WHERE email = %s
                    ORDER BY id;
                """, (email,))
                rows = cur.fetchall()

                for idx, (row_id,) in enumerate(rows):
                    if idx == 0:
                        continue
                    new_email = f"{email}_duplicate_{row_id}"
                    cur.execute("""
                        UPDATE children_management_driver
                        SET email = %s
                        WHERE id = %s;
                    """, (new_email, row_id))

            # Commit the changes
            conn.commit()
            print("Duplicates resolved successfully.")

        # Close the cursor and connection
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect()
