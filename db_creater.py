import os

import psycopg2

from dotenv import load_dotenv

load_dotenv()

"""
    Такой вариант наполнения БД как по мне кустапный и не самый эффективный, но и использоваться этот скрипт будет 
    только для тестирования бота и его функциональности, но-этому прошу не судить строго))
"""

conn = psycopg2.connect(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_LOGIN'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cursor = conn.cursor()

create_table = """
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY NOT NULL,
    username VARCHAR(32),
    first_name VARCHAR(32),
    last_name VARCHAR(32),
    registration_date TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS Categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS Products (
    product_id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES Categories(category_id),
    name VARCHAR(32),
    image_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS PackageSizes (
    package_size_id SERIAL PRIMARY KEY,
    weight VARCHAR(2),
    UNIQUE (weight)
);

CREATE TABLE IF NOT EXISTS Prices (
    price_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES Products(product_id),
    package_size_id INTEGER REFERENCES PackageSizes(package_size_id),
    price DECIMAL
);

TRUNCATE TABLE PackageSizes, Categories, Prices, Products;

INSERT INTO Categories (name)
VALUES ('Кошка'), ('Собака');

INSERT INTO PackageSizes (weight)
VALUES ('1'), ('3'), ('5'), ('15'), ('25');

INSERT INTO Products (category_id, name, image_url)
VALUES ((SELECT category_id FROM Categories WHERE name = 'Кошка'), 'Purina ONE', 'https://petobzor.com/wp-content/uploads/2017/09/Suhoj-korm-Purina-One-dlya-sterilizovannyh-koshek.jpg');

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Purina ONE'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '1'),
  249
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Purina ONE'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '3'),
  649
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Purina ONE'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '5'),
  999
);

INSERT INTO Products (category_id, name, image_url)
VALUES ((SELECT category_id FROM Categories WHERE name = 'Собака'), 'Chappi', 'https://main-cdn.sbermegamarket.ru/big1/hlr-system/-20/513/448/141/111/103/8/100001276610b0.jpg');

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Chappi'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '1'),
  300
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Chappi'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '3'),
  750
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Chappi'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '25'),
  4349
);

INSERT INTO Products (category_id, name, image_url)
VALUES ((SELECT category_id FROM Categories WHERE name = 'Собака'), 'Pedigree', 'https://4lapy.ru/resize/800x800/upload/iblock/fcf/fcf0a9243e5db9c8e6f321f0879e54e4.JPG');

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Pedigree'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '1'),
  379
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Pedigree'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '3'),
  850
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Pedigree'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '5'),
  1299
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Pedigree'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '15'),
  3249
);

INSERT INTO Prices (product_id, package_size_id, price)
VALUES (
  (SELECT product_id FROM Products WHERE name = 'Pedigree'),
  (SELECT package_size_id FROM PackageSizes WHERE weight = '25'),
  5199
);
"""

cursor.execute(create_table)
conn.commit()
