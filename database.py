import os
import psycopg
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#PostgreSQL database connection 
def get_connection():
    """Create and return a PostgreSQL connection using psycopg."""
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "hospital_management"),
        user=os.getenv("DB_USER", "shristirai"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", 5432))
    )

    #Test the database connection
if __name__ == "__main__":
    try:
        with get_connection() as connection:
            print("Database connection successful.")

    except psycopg.Error as error:
        print(f"Database connection failed: {error}")
       