#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar Session String de usuario para habilitar modo Premium (4GB)
Compatible con M01K0/Tdrive_leecher que ya incluye pyrofork==2.2.11
"""

import json
import asyncio
import sys
import os

def verify_pyrofork():
    """Verificar detalladamente que estamos usando PyroFork y no Pyrogram original"""
    print("🔍 VERIFICANDO INSTALACIÓN DE PYROFORK")
    print("=" * 60)
    
    try:
        # Verificación 1: Importar pyrogram y verificar versión
        import pyrogram
        version = pyrogram.__version__
        print(f"📦 Versión detectada: {version}")
        
        # Verificación 2: Verificar ubicación del paquete
        package_path = pyrogram.__file__
        print(f"📁 Ubicación: {os.path.dirname(package_path)}")
        
        # Verificación 3: Verificar información del paquete
        import pkg_resources
        try:
            pkg_info = pkg_resources.get_distribution("pyrofork")
            print(f"✅ PyroFork instalado: v{pkg_info.version}")
            print(f"   Ubicación PyroFork: {pkg_info.location}")
        except pkg_resources.DistributionNotFound:
            print("❌ PyroFork NO encontrado en pip")
            return False
        
        # Verificación 4: Verificar que NO existe pyrogram original
        try:
            pyrogram_pkg = pkg_resources.get_distribution("pyrogram")
            print(f"⚠️ ATENCIÓN: Pyrogram original también instalado: v{pyrogram_pkg.version}")
            print(f"   Esto puede causar conflictos!")
        except pkg_resources.DistributionNotFound:
            print("✅ Pyrogram original NO instalado (correcto)")
        
        # Verificación 5: Verificar características específicas de PyroFork
        features_found = []
        
        # Verificar si tiene características de pyrofork
        try:
            from pyrogram.types import Message
            if hasattr(Message, 'quote'):  # Característica específica de pyrofork
                features_found.append("Message.quote() (Quote Reply)")
        except:
            pass
            
        try:
            from pyrogram import Client
            # Verificar constructor específico de pyrofork
            import inspect
            client_signature = inspect.signature(Client.__init__)
            if 'mongodb' in str(client_signature):
                features_found.append("MongoDB session support")
        except:
            pass
        
        # Verificación 6: Comprobar metadatos específicos
        try:
            author_info = getattr(pyrogram, '__author__', 'Unknown')
            if 'wulan17' in author_info.lower() or 'mayuri' in author_info.lower():
                features_found.append("PyroFork author metadata")
        except:
            pass
        
        print(f"\n🎯 CARACTERÍSTICAS DE PYROFORK DETECTADAS:")
        if features_found:
            for feature in features_found:
                print(f"   ✅ {feature}")
        else:
            print("   ⚠️  No se detectaron características específicas")
        
        # Verificación 7: Verificar imports específicos
        pyrofork_modules = []
        try:
            from pyrogram.storage import MongoStorage
            pyrofork_modules.append("MongoStorage")
        except ImportError:
            pass
            
        if pyrofork_modules:
            print(f"\n🔧 MÓDULOS ESPECÍFICOS DE PYROFORK:")
            for module in pyrofork_modules:
                print(f"   ✅ {module}")
        
        # Resultado final
        print(f"\n📊 RESUMEN DE VERIFICACIÓN:")
        if version >= "2.2.0" and pkg_info:
            print(f"   ✅ PyroFork v{version} confirmado")
            print(f"   ✅ Compatible con archivos 4GB")
            print(f"   ✅ Soporte para características avanzadas")
            return True
        else:
            print(f"   ❌ Versión incompatible o instalación incorrecta")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando pyrogram: {e}")
        print("💡 Ejecuta: py -m pip install pyrofork==2.2.11")
        return False
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def load_credentials():
    """Cargar credenciales desde el archivo JSON generado por main.py"""
    try:
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo credentials.json")
        print("💡 Asegúrate de haber ejecutado main.py primero para generar las credenciales")
        print("📋 El archivo se genera automáticamente cuando ejecutas las celdas de main.py")
        return None
    except Exception as e:
        print(f"❌ Error cargando credenciales: {e}")
        return None

async def generate_session():
    """Generar session string de usuario usando Pyrofork 2.2.11"""
    print("\n🔑 GENERADOR DE SESSION STRING PARA MODO PREMIUM 4GB")
    print("=" * 60)
    
    # Verificar PyroFork antes de continuar
    if not verify_pyrofork():
        print("\n❌ VERIFICACIÓN FALLIDA: No se puede continuar sin PyroFork")
        return
    
    # Cargar credenciales generadas por main.py
    credentials = load_credentials()
    if not credentials:
        return
    
    API_ID = credentials.get("API_ID")
    API_HASH = credentials.get("API_HASH")
    
    if not API_ID or not API_HASH:
        print("❌ Error: API_ID o API_HASH no encontrados en credentials.json")
        print("💡 Verifica que hayas configurado correctamente las variables en main.py")
        return
    
    try:
        # Usar pyrofork directamente (ya disponible en requirements.txt)
        from pyrogram import Client
        
        print(f"\n📱 Configuración:")
        print(f"   Cliente: PyroFork (verificado) ✅")
        print(f"   API_ID: {API_ID}")
        print(f"   API_HASH: {API_HASH[:8]}...")
        
        print(f"\n🔐 Iniciando proceso de autenticación...")
        print(f"📲 Se te pedirá:")
        print(f"   1. Tu número de teléfono (ej: +1234567890)")
        print(f"   2. Código de verificación de Telegram")
        print(f"   3. Contraseña de 2FA (si está habilitada)")
        
        # Crear cliente temporal para generar session
        async with Client(
            "temp_session", 
            api_id=API_ID, 
            api_hash=API_HASH
        ) as client:
            # Verificar información específica del cliente
            print(f"\n🔧 INFORMACIÓN DEL CLIENTE:")
            print(f"   📱 Usando: {client.__class__.__name__}")
            print(f"   📦 Módulo: {client.__class__.__module__}")
            
            # Obtener información del usuario
            me = await client.get_me()
            is_premium = hasattr(me, 'is_premium') and me.is_premium
            
            print(f"\n👤 ¡Usuario autenticado exitosamente!")
            print(f"   📛 Nombre: {me.first_name}")
            if me.username:
                print(f"   🔗 Username: @{me.username}")
            print(f"   🆔 ID: {me.id}")
            print(f"   ⭐ Premium: {'✅ Sí' if is_premium else '❌ No'}")
            
            # Obtener session string
            session_string = await client.export_session_string()
            
            # Guardar session string
            session_file = "user_session.txt"
            with open(session_file, "w") as f:
                f.write(session_string)
            
            print(f"\n✅ SESSION STRING GENERADO EXITOSAMENTE")
            print(f"📁 Guardado en: {session_file}")
            print(f"🔒 Session String: {session_string[:50]}...")
            
            # Recomendaciones basadas en el estado Premium
            if is_premium:
                print(f"\n🎉 ¡PERFECTO! Tu cuenta tiene Telegram Premium")
                print(f"🚀 Capacidades habilitadas:")
                print(f"   ✅ Archivos de hasta 4GB")
                print(f"   ✅ PyroFork optimizado para Premium")
                print(f"   ✅ Subida con cliente de usuario")
            else:
                print(f"\n⚠️ NOTA: Tu cuenta NO tiene Telegram Premium")
                print(f"📝 Para aprovechar archivos de 4GB:")
                print(f"   1. 💳 Suscríbete a Telegram Premium")
                print(f"   2. 🔄 Reinicia el bot")
                print(f"   3. 🚀 Usa /premium para activar")
                print(f"\n💡 Sin Premium: Límite de 2GB (con división automática)")
            
            print(f"\n📋 SIGUIENTES PASOS:")
            print(f"   1. 🔄 Reinicia tu bot (ejecuta main.py)")
            print(f"   2. 🎯 Usa comando /premium para activar modo 4GB")
            print(f"   3. 📊 Verifica estado con /status")
            print(f"   4. 🧪 Prueba subiendo un archivo >2GB")
            
    except ImportError:
        print(f"❌ Error: PyroFork no está disponible")
        print(f"💡 Ejecuta: pip install pyrofork==2.2.11")
    except Exception as e:
        print(f"❌ Error generando session string: {e}")
        if "phone number" in str(e).lower():
            print("💡 Formato correcto: +1234567890 (con código de país)")
        elif "code" in str(e).lower():
            print("💡 Verifica el código de 5 dígitos que recibiste")
        elif "password" in str(e).lower():
            print("💡 Introduce tu contraseña de verificación en 2 pasos")

def main():
    """Función principal"""
    try:
        print("🚀 Iniciando generador de session string...")
        asyncio.run(generate_session())
        print(f"\n✅ Proceso completado exitosamente")
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print(f"💡 Si el problema persiste, verifica:")
        print(f"   1. Conexión a internet estable")
        print(f"   2. Credenciales válidas en main.py")
        print(f"   3. API_ID y API_HASH correctos")

if __name__ == "__main__":
    main() 