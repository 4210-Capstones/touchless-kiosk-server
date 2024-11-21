import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(__file__).absolute().parent.parent.absolute().joinpath('.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

database_url = os.getenv("DATABASE_URL")
jwt_key_path = os.getenv("JWT_KEY_PATH")