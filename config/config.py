import os
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN: str = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("Токен бота не найден в .env файле")

ADMIN = int(os.getenv("ADMIN"))
