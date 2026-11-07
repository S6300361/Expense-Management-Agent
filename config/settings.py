import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

APP_NAME = os.getenv("APP_NAME", "Expense Management Agent")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(BASE_DIR / "database" / "expenses.db")
)

DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "PKR")