# copyright 2023 © M01K0 | https://github.com/M01K0/tl_script


import os
import logging
from PIL import Image
from asyncio import sleep
from os import path as ospath
from datetime import datetime
from pyrogram.errors import FloodWait
from colab_leecher import colab_bot, OWNER
from colab_leecher.utility.variables import BOT, Transfer, BotTimes, Messages, MSG, Paths
from colab_leecher.utility.helper import sizeUnit, fileType, getTime, status_bar, thumbMaintainer, videoExtFix

# Cliente de usuario global para archivos grandes
user_client = None

def get_upload_client(file_size):
    """
    Seleccionar el cliente correcto para la subida basándose en el tamaño del archivo
    """
    global user_client
    
    # Si el archivo es mayor al umbral y tenemos cliente de usuario premium
    if file_size > BOT.Options.large_file_threshold and BOT.Options.is_premium_user and BOT.Options.user_session_string:
        # Crear cliente de usuario si no existe
        if user_client is None:
            try:
                # Usar pyrofork directamente (ya disponible en requirements.txt==2.2.11)
                from pyrofork import Client
                user_client = Client(
                    "user_upload",
                    api_id=colab_bot.api_id,
                    api_hash=colab_bot.api_hash,
                    session_string=BOT.Options.user_session_string
                )
                logging.info("✅ Cliente de usuario (Pyrofork 2.2.11) configurado para archivos >2GB")
            except ImportError:
                # Fallback extremadamente improbable
                from pyrogram import Client
                user_client = Client(
                    "user_upload",
                    api_id=colab_bot.api_id,
                    api_hash=colab_bot.api_hash,
                    session_string=BOT.Options.user_session_string
                )
                logging.warning("⚠️ Fallback a Pyrogram - funcionalidad limitada")
        
        # Retornar cliente de usuario para archivos grandes
        if user_client and BOT.Options.is_premium_user:
            logging.info(f"📤 Usando cliente USUARIO (4GB) para archivo: {sizeUnit(file_size)}")
            return user_client
    
    # Retornar cliente bot para archivos pequeños o sin premium
    logging.info(f"📤 Usando cliente BOT (2GB) para archivo: {sizeUnit(file_size)}")
    return colab_bot

async def progress_bar(current, total):
    global status_msg, status_head
    upload_speed = 4 * 1024 * 1024
    elapsed_time_seconds = (datetime.now() - BotTimes.task_start).seconds
    if current > 0 and elapsed_time_seconds > 0:
        upload_speed = current / elapsed_time_seconds
    eta = (Transfer.total_down_size - current - sum(Transfer.up_bytes)) / upload_speed
    percentage = (current + sum(Transfer.up_bytes)) / Transfer.total_down_size * 100
    
    # Mostrar motor de subida correcto
    engine = "Pyrofork 4GB ⚡" if BOT.Options.is_premium_user and BOT.Options.premium_mode else "Pyrogram 2GB 🚀"
    
    await status_bar(
        down_msg=Messages.status_head,
        speed=f"{sizeUnit(upload_speed)}/s",
        percentage=percentage,
        eta=getTime(eta),
        done=sizeUnit(current + sum(Transfer.up_bytes)),
        left=sizeUnit(Transfer.total_down_size),
        engine=engine,
    )


async def upload_file(file_path, real_name):
    global Transfer, MSG, user_client
    BotTimes.task_start = datetime.now()
    caption = f"<{BOT.Options.caption}>{BOT.Setting.prefix} {real_name} {BOT.Setting.suffix}</{BOT.Options.caption}>"
    type_ = fileType(file_path)
    
    # Obtener tamaño del archivo
    file_size = ospath.getsize(file_path)
    
    # Seleccionar cliente apropiado
    upload_client = get_upload_client(file_size)
    
    # Iniciar cliente de usuario si es necesario
    client_started = False
    if upload_client == user_client and not upload_client.is_connected:
        try:
            await upload_client.start()
            client_started = True
            logging.info("🔑 Cliente de usuario iniciado para subida >2GB")
        except Exception as e:
            logging.error(f"❌ Error iniciando cliente de usuario: {e}")
            # Fallback al cliente bot
            upload_client = colab_bot
            logging.info("🔄 Fallback a cliente bot")

    f_type = type_ if BOT.Options.stream_upload else "document"

    # Upload the file
    try:
        if f_type == "video":
            # For Renaming to mp4
            if not BOT.Options.stream_upload:
                file_path = videoExtFix(file_path)
            # Generate Thumbnail and Get Duration
            thmb_path, seconds = thumbMaintainer(file_path)
            with Image.open(thmb_path) as img:
                width, height = img.size

            MSG.sent_msg = await upload_client.send_video(
                chat_id=OWNER,
                video=file_path,
                supports_streaming=True,
                width=width,
                height=height,
                caption=caption,
                thumb=thmb_path,
                duration=int(seconds),
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id,
            )

        elif f_type == "audio":
            thmb_path = None if not ospath.exists(Paths.THMB_PATH) else Paths.THMB_PATH
            MSG.sent_msg = await upload_client.send_audio(
                chat_id=OWNER,
                audio=file_path,
                caption=caption,
                thumb=thmb_path,  # type: ignore
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id,
            )

        elif f_type == "document":
            if ospath.exists(Paths.THMB_PATH):
                thmb_path = Paths.THMB_PATH
            elif type_ == "video":
                thmb_path, _ = thumbMaintainer(file_path)
            else:
                thmb_path = None

            MSG.sent_msg = await upload_client.send_document(
                chat_id=OWNER,
                document=file_path,
                caption=caption,
                thumb=thmb_path,  # type: ignore
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id,
            )

        elif f_type == "photo":
            MSG.sent_msg = await upload_client.send_photo(
                chat_id=OWNER,
                photo=file_path,
                caption=caption,
                progress=progress_bar,
                reply_to_message_id=MSG.sent_msg.id,
            )

        Transfer.sent_file.append(MSG.sent_msg)
        Transfer.sent_file_names.append(real_name)
        
        # Log del éxito con información del cliente usado
        client_info = "Usuario (Premium 4GB)" if upload_client == user_client else "Bot (Estándar 2GB)"
        logging.info(f"✅ Archivo subido exitosamente con cliente {client_info}: {real_name} ({sizeUnit(file_size)})")

    except FloodWait as e:
        logging.warning(f"FloodWait: Waiting {e.value} Seconds Before Trying Again.")
        await sleep(e.value)  # Wait dynamic FloodWait seconds before Trying Again
        await upload_file(file_path, real_name)
    except Exception as e:
        logging.error(f"Error When Uploading : {e}")
        # Si falla con cliente de usuario, intentar con bot como fallback
        if upload_client == user_client:
            logging.info("🔄 Reintentando con cliente bot como fallback...")
            try:
                if f_type == "document":
                    MSG.sent_msg = await colab_bot.send_document(
                        chat_id=OWNER,
                        document=file_path,
                        caption=caption,
                        thumb=thmb_path if 'thmb_path' in locals() else None,
                        progress=progress_bar,
                        reply_to_message_id=MSG.sent_msg.id,
                    )
                    Transfer.sent_file.append(MSG.sent_msg)
                    Transfer.sent_file_names.append(real_name)
                    logging.info(f"✅ Archivo subido con cliente bot (fallback): {real_name}")
            except Exception as e2:
                logging.error(f"❌ Error también con cliente bot: {e2}")
    
    finally:
        # Cerrar cliente de usuario si lo iniciamos
        if client_started and upload_client == user_client:
            try:
                await upload_client.stop()
                logging.info("🔒 Cliente de usuario detenido")
            except:
                pass
