import dotenv
import psycopg2
import os

def connect_db():
    res = dotenv.load_dotenv()
    if not res:
        raise Exception("Failed to laod dotenv")
    
    conn = psycopg2.connect(
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host="172.30.240.1",
        port="5432",
    )

    conn.autocommit = True

    return conn