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
        print("Пользователь уже существует!")


async def check_user_exists(conn, user_id):
    query = "SELECT EXISTS (SELECT 1 FROM users WHERE user_id = $1)"
    exists = await conn.fetchval(query, user_id)
    return exists


import asyncpg


async def get_product(conn, category_name, size):
    query = """
    SELECT 
        p.name AS product_name,
        ps.weight,
        pr.price,
        p.image_url
    FROM Products p
        JOIN Categories c ON p.category_id = c.category_id
        JOIN Prices pr ON p.product_id = pr.product_id
        JOIN PackageSizes ps ON pr.package_size_id = ps.package_size_id
    WHERE 
        c.name = $1
        AND ps.weight = $2;
    """

    try:
        result = await conn.fetch(query, category_name, size)
        return result
    except asyncpg.exceptions.PostgresError as e:
        print(f"При выполнении запроса произошла ошибка: {e}")
        return []
