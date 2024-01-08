import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables

# MongoDB
DB_MONGODB_URL = os.getenv("DB_MONGODB_URL")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_TIME_EXPIRE = 60 * 3 # minutes
