import mysql.connector
# -------------------------
# API Configuration
# -------------------------
class APIConfig:
    HOST = "aerodatabox.p.rapidapi.com"
    KEY = "4bccebdf7bmsh907f18e38b6fc33p1632cejsnf2d46e00dc6b"

    HEADERS = {
        "x-rapidapi-key": KEY,
        "x-rapidapi-host": HOST
    }
# -------------------------
# Database Configuration
# -------------------------
class DBConfig:
    HOST = "localhost"
    USER = "root"
    PASSWORD = "Bindu@123"
    DATABASE = "air_tracker"

    @staticmethod
    def get_connection():
        #Return a new MySQL connection and cursor.
        connection = mysql.connector.connect(
            host=DBConfig.HOST,
            user=DBConfig.USER,
            password=DBConfig.PASSWORD,
            database=DBConfig.DATABASE
        )
        cursor = connection.cursor()
        return connection, cursor
