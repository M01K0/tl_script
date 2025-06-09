# copyright 2023 © M01K0 | https://github.com/M01K0/tl_script

import logging, json, sys

# 🔧 IMPORTACIÓN OPCIONAL DE UVLOOP - Compatible con Google Colab
try:
    from uvloop import install
    install()
    print("⚡ uvloop activado - Rendimiento optimizado")
except ImportError:
    print("⚠️ uvloop no disponible - Usando event loop estándar")
    print("💡 Para mejor rendimiento: pip install uvloop")
except Exception as e:
    print(f"⚠️ uvloop falló: {str(e)[:50]}... - Usando event loop estándar")

# 🔍 DETECCIÓN MEJORADA DE PYROFORK - Similar a generate_user_session.py
PYROFORK_AVAILABLE = False
PYROGRAM_VERSION = "unknown"

print("🔍 Detectando librerías disponibles...")

try:
    import pyrofork
    from pyrofork import Client
    PYROFORK_AVAILABLE = True
    PYROGRAM_VERSION = pyrofork.__version__
    print(f"✅ Pyrofork {PYROGRAM_VERSION} detectado - Soporte 4GB habilitado")
    print("🚀 Motor optimizado para archivos grandes cargado correctamente")
except ImportError as e:
    try:
        import pyrogram
        from pyrogram import Client
        PYROGRAM_VERSION = pyrogram.__version__
        print(f"⚠️ Pyrofork no encontrado, usando Pyrogram {PYROGRAM_VERSION} estándar - limitado a 2GB")
        print("💡 Para habilitar 4GB: pip install --force-reinstall pyrofork==2.2.11")
    except ImportError:
        print("❌ Error crítico: No se encontró ni Pyrofork ni Pyrogram")
        print("💊 Solución: pip install pyrofork==2.2.11")
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

colab_bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Configurar las variables globales del bot con el soporte detectado
from .utility.variables import BOT

# 🔧 CONFIGURACIÓN AVANZADA BASADA EN CAPACIDADES DETECTADAS
if PYROFORK_AVAILABLE:
    BOT.Options.max_file_size = 4194304000  # 4GB con Pyrofork
    BOT.Options.large_file_threshold = 2097152000  # 2GB umbral para cambiar a cliente usuario
    print("🚀 Límite máximo configurado: 4GB con Pyrofork")
    print("📊 Sistema listo para modo Premium")
else:
    BOT.Options.max_file_size = 2097152000  # 2GB estándar
    BOT.Options.large_file_threshold = 2097152000  # Mismo umbral
    print("📊 Límite máximo configurado: 2GB con Pyrogram estándar")
    print("💡 Para 4GB instala: pip install --force-reinstall pyrofork==2.2.11")

# 🌟 VARIABLES GLOBALES PARA PREMIUM
BOT.Options.pyrofork_available = PYROFORK_AVAILABLE
BOT.Options.pyrogram_version = PYROGRAM_VERSION

print(f"📋 Configuración completada:")
print(f"   🔧 Motor: {'Pyrofork' if PYROFORK_AVAILABLE else 'Pyrogram'} {PYROGRAM_VERSION}")
print(f"   📊 Límite: {BOT.Options.max_file_size // (1024*1024*1024)}GB")
print(f"   🌟 Premium Ready: {'✅ Sí' if PYROFORK_AVAILABLE else '❌ No'}")
