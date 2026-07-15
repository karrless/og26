import os
from dotenv import load_dotenv

load_dotenv()

def get_env(name: str):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"В .env нет значения {name}")

DB_URI = get_env("DB_URI")

LOG_LEVEL = get_env("LOG_LEVEL")

GOOGLE_CREDENTIALS_PATH = get_env("GOOGLE_CREDENTIALS_PATH")

SPREADSHEET_ID = get_env("SPREADSHEET_ID")

VK_API1 = get_env("VK_API1")
VK_API2 = get_env("VK_API2")

TG_TOKEN = get_env("TG_TOKEN")

TG_SOCKS = get_env("TG_SOCKS")