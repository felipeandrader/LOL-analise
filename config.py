import os
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
REGIAO_BR = os.getenv("REGIAO_BR", "br1")
REGIAO_AMERICAS = os.getenv("REGIAO_AMERICAS", "americas")

if not RIOT_API_KEY:
    raise ValueError("chave'RIOT_API_KEY' não encontrada.")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "riot_data")

if not DB_PASS:
    raise ValueError("senha não encontrada no arquivo .env!")

DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"