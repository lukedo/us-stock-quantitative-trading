import os
from dotenv import load_dotenv

load_dotenv()

OPEND_HOST = os.getenv("FUTU_OPEND_HOST", "127.0.0.1")
OPEND_PORT = int(os.getenv("FUTU_OPEND_PORT", "11111"))
TRD_ENV = os.getenv("FUTU_TRD_ENV", "SIMULATE")
DEFAULT_MARKET = os.getenv("FUTU_DEFAULT_MARKET", "US")
ACC_ID = os.getenv("FUTU_ACC_ID", "")
SECURITY_FIRM = os.getenv("FUTU_SECURITY_FIRM", "")

CACHE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cache.db")
