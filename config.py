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