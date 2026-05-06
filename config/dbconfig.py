import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file next to this file
load_dotenv(Path(__file__).with_name(".env"))

# Database configuration settings
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'wsaa')
}