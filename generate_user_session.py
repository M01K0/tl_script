#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar Session String de usuario para habilitar modo Premium (4GB)
Compatible con M01K0/Tdrive_leecher que ya incluye pyrofork==2.2.11
"""

import json
import asyncio

def load_credentials():
    """Cargar credenciales desde el archivo JSON generado por main.py"""
    try:
        with open('/content/Tdrive_leecher/credentials.json', 'r') as f:
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
    print("🔑 GENERADOR DE SESSION STRING PARA MODO PREMIUM 4GB")
    print("=" * 60)
    print("📦 Detectado: Pyrofork 2.2.11 (soporte completo 4GB)")
    
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
        from pyrofork import Client
        
        print(f"\n📱 Configuración:")
        print(f"   Cliente: Pyrofork 2.2.11 ✅")
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
            session_file = "/content/Tdrive_leecher/user_session.txt"
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
                print(f"   ✅ Pyrofork 2.2.11 optimizado")
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
        print(f"❌ Error: Pyrofork no está disponible")
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