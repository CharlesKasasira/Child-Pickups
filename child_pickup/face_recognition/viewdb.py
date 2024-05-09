import sqlite3

def view_data():
    try:
        conn = sqlite3.connect("sqlite.db")
        cursor = conn.execute("SELECT * FROM STUDENTS")
        for row in cursor:
            print("ID:", row[0])
            print("Name:", row[1])
            print("Age:", row[2])
        conn.close()
    except sqlite3.Error as e:
        print("Error:", e)

# Call the view_data function to print the data
view_data()
