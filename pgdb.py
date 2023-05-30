import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()


async def create_db_connection():
    conn = await asyncpg.connect(
        user=os.getenv('DB_LOGIN'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn


async def insert_data(conn, user_id, username, first_name, last_name, registration_date):
    exists = await check_user_exists(conn, user_id)
    if not exists:
        insert_query = """
        INSERT INTO users (user_id, username, first_name, last_name, registration_date)
        VALUES ($1, $2, $3, $4, $5)
        """
        await conn.execute(insert_query, user_id, username, first_name, last_name, registration_date)
    else:
        print("User already exists")


async def check_user_exists(conn, user_id):
    query = "SELECT EXISTS (SELECT 1 FROM users WHERE user_id = $1)"
    exists = await conn.fetchval(query, user_id)
    return exists
