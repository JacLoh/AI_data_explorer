import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "PW_placeholder",  
    "database": "aiexplorer"
}


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
