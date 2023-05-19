import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


QUESTIONS_URL = "https://jservice.io/api/random?count={}"
CHUNK_SIZE = 1024 * 1024 * 5  # 5 megabytes
