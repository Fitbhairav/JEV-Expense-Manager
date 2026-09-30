import os

from dotenv import load_dotenv

load_dotenv()


JEV_API_KEY = os.getenv("JEV_API_KEY")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./expenses.db"
)

MOCK_JEV = os.getenv(
    "MOCK_JEV",
    "false"
).lower() in ("true", "1", "t", "yes")

