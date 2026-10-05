import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def main():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set.")

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            result = cursor.fetchone()

    print("PostgreSQL connection successful!")
    print(result[0])


if __name__ == "__main__":
    main()