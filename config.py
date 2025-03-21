import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "#mysqlPW1107",  
    "database": "aiexplorer"
}


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
