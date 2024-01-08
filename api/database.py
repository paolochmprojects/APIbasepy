from motor.motor_asyncio import AsyncIOMotorClient
from logging import getLogger
import api.settings as settings

logger = getLogger("uvicorn")

client = AsyncIOMotorClient(settings.DB_MONGODB_URL)

db = client.get_database("odontoDB")