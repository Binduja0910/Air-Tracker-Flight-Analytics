import mysql.connector

def test_connection():
    try:
        # Connect to MySQL database
        Connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Bindu@123",   
            database="air_tracker"
        )
        cursor = Connect.cursor()

        # Show all tables in the airtracker database
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        print("✅ Connected successfully!")
        print("Tables in airtracker database:")
        for table in tables:
            print("-", table[0])

        cursor.close()
        Connect.close()

    except mysql.connector.Error as err:
        print("❌ Error:", err)

if __name__ == "__main__":
    test_connection()
