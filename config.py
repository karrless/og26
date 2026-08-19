import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"В .env нет значения {name}")


DB_URI = get_env("DB_URI")

USE_SSH_TUNNEL = os.getenv("USE_SSH_TUNNEL", "false").lower() == "true"

SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = int(os.getenv("SSH_PORT", "22"))
SSH_LOGIN = os.getenv("SSH_LOGIN")
SSH_PASS = os.getenv("SSH_PASS")

DB_REMOTE_HOST = os.getenv("DB_REMOTE_HOST", "127.0.0.1")
DB_REMOTE_PORT = int(os.getenv("DB_REMOTE_PORT", "5432"))
SSH_LOCAL_BIND_PORT = int(os.getenv("SSH_LOCAL_BIND_PORT", "6543"))

LOG_LEVEL = get_env("LOG_LEVEL")

GOOGLE_CREDENTIALS_PATH = get_env("GOOGLE_CREDENTIALS_PATH")

SPREADSHEET_ID = get_env("SPREADSHEET_ID")

VK_API1 = get_env("VK_API1")
VK_API2 = get_env("VK_API2")

TG_TOKEN = get_env("TG_TOKEN")

TG_SOCKS = get_env("TG_SOCKS")

VK_MODERATOR_CHAT_PEER_ID = get_env("VK_MODERATOR_CHAT_PEER_ID")
MODER_LIMIT = int(get_env("MODER_LIMIT"))

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_USERNAME = get_env('API_USERNAME')
API_PASSWORD_HASH = get_env('API_PASSWORD_HASH')
JWT_SECRET = get_env('JWT_SECRET')
JWT_EXPIRE_MINUTES = int(get_env('JWT_EXPIRE_MINUTES'))

FRONT_URI = os.getenv("FRONT_HOST", "http://localhost:5137")
