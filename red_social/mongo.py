import os
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "socialcaz")  # tu base de datos

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI no está configurado en variables de entorno")

_client = MongoClient(MONGODB_URI)
db = _client[MONGO_DB_NAME]

# Colecciones usadas
users_coll = db["usuarios"]  # tu colección de usuarios
posts_coll = db["posts"]
audit_coll = db["audit_logs"]
