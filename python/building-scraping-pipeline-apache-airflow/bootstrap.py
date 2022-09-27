import os

import psycopg2

from messenger import Queue
from oxylabs import Client

DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_USER = os.getenv('DB_USER', 'airflow')
DB_PASS = os.getenv('DB_PASS', 'airflow')
DB_NAME = os.getenv('DB_NAME', 'scraper')
OXYLABS_USERNAME = os.getenv('OXYLABS_USERNAME', 'your-oxylabs-username')
OXYLABS_PASSWORD = os.getenv('OXYLABS_PASSWORD', 'your-oxylabs-password')

connection = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)

queue = Queue(
    connection
)

client = Client(
    OXYLABS_USERNAME,
    OXYLABS_PASSWORD,
)