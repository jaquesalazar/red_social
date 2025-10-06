import os
from pymongo import MongoClient
from urllib.parse import quote_plus

MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "socialcaz")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI no está configurado en variables de entorno")

_client = MongoClient(MONGODB_URI)
db = _client[MONGO_DB_NAME]

# colecciones usadas
users_coll = db["personal"]          # conforme a tu colección 'personal'
posts_coll = db["posts"]
audit_coll = db["audit_logs"]