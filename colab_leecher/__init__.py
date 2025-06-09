# copyright 2023 © M01K0 | https://github.com/M01K0/tl_script

import logging, json, sys, os

def verify_pyrofork_colab():
    """
    🔍 VERIFICACIÓN EXHAUSTIVA DE PYROFORK PARA GOOGLE COLAB
    Adaptado del sistema local para el entorno Colab
    """
    print("🔍 VERIFICACIÓN EXHAUSTIVA DE PYROFORK - GOOGLE COLAB")
    print("=" * 70)
    
    verification_results = {
        'pyrofork_available': False,
        'version': 'unknown',
        'features_found': [],
        'modules_found': [],
        'is_premium_ready': False,
        'max_file_size': 2097152000,  # 2GB por defecto
        'warnings': []
    }
    
    try:
        # 🔍 Verificación 1: Importar y verificar versión
        print("📦 Verificando instalación de bibliotecas...")
        
        import pyrogram
        version = pyrogram.__version__
        package_path = pyrogram.__file__
        
        print(f"   ✅ Versión detectada: {version}")
        print(f"   📁 Ubicación: {os.path.dirname(package_path)}")
        
        verification_results['version'] = version
        
        # 🔍 Verificación 2: Verificar información de paquetes pip
        try:
            import pkg_resources
            
            # Verificar PyroFork
            try:
                pkg_info = pkg_resources.get_distribution("pyrofork")
                print(f"   ✅ PyroFork detectado: v{pkg_info.version}")
                print(f"   📍 Ubicación PyroFork: {pkg_info.location}")
                verification_results['pyrofork_available'] = True
            except pkg_resources.DistributionNotFound:
                print("   ❌ PyroFork NO encontrado en pip")
                verification_results['warnings'].append("PyroFork no está instalado")
            
            # Verificar Pyrogram original (no debería existir)
            try:
                pyrogram_pkg = pkg_resources.get_distribution("pyrogram")
                print(f"   ⚠️ ATENCIÓN: Pyrogram original detectado: v{pyrogram_pkg.version}")
                verification_results['warnings'].append("Conflicto: Pyrogram original también instalado")
            except pkg_resources.DistributionNotFound:
                print("   ✅ Pyrogram original NO instalado (correcto)")
                
        except ImportError:
            print("   ⚠️ pkg_resources no disponible - verificación limitada")
        
        # 🔍 Verificación 3: Características específicas de PyroFork
        print("\n🎯 Verificando características específicas de PyroFork...")
        
        # Verificar Message.quote (Quote Reply)
        try:
            from pyrogram.types import Message
            if hasattr(Message, 'quote'):
                verification_results['features_found'].append("Message.quote() - Quote Reply")
                print("   ✅ Quote Reply support detectado")
        except Exception:
            pass
        
        # Verificar soporte MongoDB
        try:
            from pyrogram import Client
            import inspect
            client_signature = inspect.signature(Client.__init__)
            if 'mongodb' in str(client_signature).lower():
                verification_results['features_found'].append("MongoDB session support")
                print("   ✅ MongoDB session support detectado")
        except Exception:
            pass
        
        # Verificar metadatos del autor
        try:
            author_info = getattr(pyrogram, '__author__', 'Unknown')
            if any(name in author_info.lower() for name in ['wulan17', 'mayuri', 'pyrofork']):
                verification_results['features_found'].append("PyroFork author metadata")
                print("   ✅ PyroFork author metadata detectado")
        except Exception:
            pass
        
        # 🔍 Verificación 4: Módulos específicos de PyroFork
        print("\n🔧 Verificando módulos específicos...")
        
        # MongoStorage
        try:
            from pyrogram.storage import MongoStorage
            verification_results['modules_found'].append("MongoStorage")
            print("   ✅ MongoStorage disponible")
        except ImportError:
            pass
        
        # Verificar otros módulos específicos
        try:
            from pyrogram.types import Story
            verification_results['modules_found'].append("Story support")
            print("   ✅ Story support disponible")
        except ImportError:
            pass
        
        # 🔍 Verificación 5: Determinar capacidades
        print("\n📊 Analizando capacidades...")
        
        # Lógica mejorada para determinar si es PyroFork
        is_pyrofork = (
            verification_results['pyrofork_available'] or
            len(verification_results['features_found']) >= 1 or
            len(verification_results['modules_found']) >= 1 or
            (version >= "2.2.0" and "pyrogram" in str(package_path))
        )
        
        if is_pyrofork:
            verification_results['is_premium_ready'] = True
            verification_results['max_file_size'] = 4194304000  # 4GB
            print("   ✅ PyroFork confirmado - Modo Premium habilitado")
            print("   🚀 Archivos hasta 4GB soportados")
        else:
            print("   ⚠️ Pyrogram estándar detectado - Limitado a 2GB")
            verification_results['warnings'].append("Capacidad limitada a 2GB")
        
        # 🔍 Verificación 6: TgCrypto (opcional pero recomendado)
        try:
            import tgcrypto
            print("   ✅ TgCrypto disponible - Velocidad optimizada")
        except ImportError:
            print("   ⚠️ TgCrypto no disponible - Velocidad reducida")
            verification_results['warnings'].append("TgCrypto no instalado (recomendado para velocidad)")
        
        # 📋 Resumen final
        print("\n📋 RESUMEN DE VERIFICACIÓN:")
        print(f"   🔧 Motor: {'PyroFork' if is_pyrofork else 'Pyrogram'} v{version}")
        print(f"   📊 Límite máximo: {verification_results['max_file_size'] // (1024*1024*1024)}GB")
        print(f"   🌟 Premium Ready: {'✅ Sí' if verification_results['is_premium_ready'] else '❌ No'}")
        
        if verification_results['features_found']:
            print(f"   🎯 Características: {len(verification_results['features_found'])} detectadas")
            for feature in verification_results['features_found']:
                print(f"      • {feature}")
        
        if verification_results['modules_found']:
            print(f"   🔧 Módulos especiales: {len(verification_results['modules_found'])} disponibles")
            for module in verification_results['modules_found']:
                print(f"      • {module}")
        
        if verification_results['warnings']:
            print(f"   ⚠️ Advertencias: {len(verification_results['warnings'])}")
            for warning in verification_results['warnings']:
                print(f"      • {warning}")
        
        # Recomendaciones
        print("\n💡 RECOMENDACIONES:")
        if not verification_results['is_premium_ready']:
            print("   📦 Para habilitar modo 4GB:")
            print("      !pip install --force-reinstall pyrofork==2.2.11")
        
        if 'TgCrypto no instalado' in str(verification_results['warnings']):
            print("   ⚡ Para mejor velocidad:")
            print("      !pip install tgcrypto")
        
        return verification_results
        
    except ImportError as e:
        print(f"❌ Error crítico importando pyrogram: {e}")
        print("💊 SOLUCIÓN INMEDIATA:")
        print("   !pip install pyrofork==2.2.11")
        verification_results['warnings'].append(f"Error crítico: {e}")
        return verification_results
    
    except Exception as e:
        print(f"❌ Error inesperado en verificación: {e}")
        verification_results['warnings'].append(f"Error inesperado: {e}")
        return verification_results

# 🚀 EJECUTAR VERIFICACIÓN AL INICIO
verification_result = verify_pyrofork_colab()

# 🔧 IMPORTACIONES BASADAS EN RESULTADOS
if verification_result['is_premium_ready']:
    # Usar pyrogram (que es realmente pyrofork)
    from pyrogram import Client
    print("\n🚀 Cargando PyroFork - Modo Premium activado")
else:
    try:
        from pyrogram import Client
        print("\n📊 Cargando Pyrogram estándar - Modo básico")
    except ImportError:
        print("\n❌ ERROR CRÍTICO: No se puede importar ninguna biblioteca")
        raise ImportError("Instala PyroFork: !pip install pyrofork==2.2.11")

# 🔧 IMPORTACIÓN OPCIONAL DE UVLOOP - Compatible con Google Colab
try:
    from uvloop import install
    install()
    print("⚡ uvloop activado - Rendimiento optimizado")
except ImportError:
    print("⚠️ uvloop no disponible - Usando event loop estándar")
except Exception as e:
    print(f"⚠️ uvloop falló: {str(e)[:50]}... - Usando event loop estándar")

# Read the dictionary from the txt file
try:
    with open("/content/tl_script/credentials.json", "r") as file:
        credentials = json.loads(file.read())
except FileNotFoundError:
    print("❌ Error: credentials.json no encontrado")
    print("💡 Asegúrate de que main.py se ejecutó correctamente")
    raise

API_ID = credentials["API_ID"]
API_HASH = credentials["API_HASH"]
BOT_TOKEN = credentials["BOT_TOKEN"]
OWNER = credentials["USER_ID"]
DUMP_ID = credentials["DUMP_ID"]

logging.basicConfig(level=logging.INFO)

print(f"\n🤖 Iniciando cliente bot con configuración verificada...")
colab_bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Configurar las variables globales del bot con los resultados de verificación
from .utility.variables import BOT

# 🔧 CONFIGURACIÓN AVANZADA BASADA EN VERIFICACIÓN
BOT.Options.max_file_size = verification_result['max_file_size']
BOT.Options.large_file_threshold = 2097152000  # 2GB umbral para cambiar a cliente usuario
BOT.Options.pyrofork_available = verification_result['is_premium_ready']
BOT.Options.pyrogram_version = verification_result['version']
BOT.Options.detected_features = verification_result['features_found']
BOT.Options.detected_modules = verification_result['modules_found']
BOT.Options.system_warnings = verification_result['warnings']

print(f"\n✅ CONFIGURACIÓN FINAL APLICADA:")
print(f"   🔧 Motor: {'PyroFork' if verification_result['is_premium_ready'] else 'Pyrogram'} {verification_result['version']}")
print(f"   📊 Límite máximo: {verification_result['max_file_size'] // (1024*1024*1024)}GB")
print(f"   🌟 Premium Ready: {'✅ Sí' if verification_result['is_premium_ready'] else '❌ No'}")
print(f"   📋 Sistema listo para uso en Google Colab")
print("=" * 70)
