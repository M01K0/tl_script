# copyright 2023 © M01K0 | https://github.com/M01K0/tl_script

import logging, json
from uvloop import install

# Usar Pyrofork en lugar de Pyrogram para soporte 4GB
PYROFORK_AVAILABLE = False
try:
    from pyrofork import Client
    PYROFORK_AVAILABLE = True
    print("✅ Usando Pyrofork - Soporte 4GB habilitado")
except ImportError:
    try:
        from pyrogram import Client
        print("⚠️ Pyrofork no encontrado, usando Pyrogram estándar - limitado a 2GB")
    except ImportError:
        print("❌ Error: No se encontró ni Pyrofork ni Pyrogram")
        raise

# Read the dictionary from the txt file
with open("/content/tl_script/credentials.json", "r") as file:
    credentials = json.loads(file.read())

API_ID = credentials["API_ID"]
API_HASH = credentials["API_HASH"]
BOT_TOKEN = credentials["BOT_TOKEN"]
OWNER = credentials["USER_ID"]
DUMP_ID = credentials["DUMP_ID"]

logging.basicConfig(level=logging.INFO)

install()

colab_bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Configurar las variables globales del bot con el soporte detectado
from .utility.variables import BOT

# Configurar límites basándose en Pyrofork
if PYROFORK_AVAILABLE:
    BOT.Options.max_file_size = 4194304000  # 4GB
    print("🚀 Límite máximo configurado: 4GB con Pyrofork")
else:
    BOT.Options.max_file_size = 2097152000  # 2GB
    print("📊 Límite máximo configurado: 2GB con Pyrogram estándar")
