# copyright 2024 © M01K0 | https://github.com/M01K0/tl_script


import logging, os
from pyrogram import filters
from datetime import datetime
from asyncio import sleep, get_event_loop
from colab_leecher import colab_bot, OWNER
from colab_leecher.utility.handler import cancelTask
from .utility.variables import BOT, MSG, BotTimes, Paths
from .utility.task_manager import taskScheduler, task_starter
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .utility.helper import isLink, setThumbnail, message_deleter, send_settings


src_request_msg = None


@colab_bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.delete()
    text = "**Hey There, 👋🏼 It's Colab Leecher**\n\n◲ I am a Powerful File Transloading Bot 🚀\n◲ I can Transfer Files To Telegram or Your Google Drive From Various Sources 🦐"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Repository 🦄",
                    url="https://github.com/M01K0/tl_script",
                ),
                InlineKeyboardButton("Support 💝", url="https://t.me/Colab_Leecher"),
            ],
        ]
    )
    await message.reply_text(text, reply_markup=keyboard)


@colab_bot.on_message(filters.command("tupload") & filters.private)
async def telegram_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = False

    text = "<b>⚡ Send Me DOWNLOAD LINK(s) 🔗»</b>\n\n🦀 Follow the below pattern\n\n<code>https//linktofile1.mp4\nhttps//linktofile2.mp4\n[Custom name space.mp4]\n{Password for zipping}\n(Password for unzip)</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("gdupload") & filters.private)
async def drive_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "mirror"
    BOT.Mode.ytdl = False

    text = "<b>⚡ Send Me DOWNLOAD LINK(s) 🔗»</b>\n\n🦀 Follow the below pattern\n\n<code>https//linktofile1.mp4\nhttps//linktofile2.mp4\n[Custom name space.mp4]\n{Password for zipping}\n(Password for unzip)</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("drupload") & filters.private)
async def directory_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "dir-leech"
    BOT.Mode.ytdl = False

    text = "<b>⚡ Send Me FOLDER PATH 🔗»</b>\n\n🦀 Below is an example\n\n<code>/home/user/Downloads/bot</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("ytupload") & filters.private)
async def yt_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = True

    text = "<b>⚡ Send YTDL DOWNLOAD LINK(s) 🔗»</b>\n\n🦀 Follow the below pattern\n\n<code>https//linktofile1.mp4\nhttps//linktofile2.mp4\n[Custom name space.mp4]\n{Password for zipping}</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("settings") & filters.private)
async def settings(client, message):
    if message.chat.id == OWNER:
        await message.delete()
        await send_settings(client, message, message.id, True)


@colab_bot.on_message(filters.reply)
async def setPrefix(client, message):
    global BOT, SETTING
    if BOT.State.prefix:
        BOT.Setting.prefix = message.text
        BOT.State.prefix = False

        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()
    elif BOT.State.suffix:
        BOT.Setting.suffix = message.text
        BOT.State.suffix = False

        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()


@colab_bot.on_message(filters.create(isLink) & ~filters.photo)
async def handle_url(client, message):
    global BOT

    # Reset
    BOT.Options.custom_name = ""
    BOT.Options.zip_pswd = ""
    BOT.Options.unzip_pswd = ""

    if src_request_msg:
        await src_request_msg.delete()
    if BOT.State.task_going == False and BOT.State.started:
        temp_source = message.text.splitlines()

        # Check for arguments in message
        for _ in range(3):
            if temp_source[-1][0] == "[":
                BOT.Options.custom_name = temp_source[-1][1:-1]
                temp_source.pop()
            elif temp_source[-1][0] == "{":
                BOT.Options.zip_pswd = temp_source[-1][1:-1]
                temp_source.pop()
            elif temp_source[-1][0] == "(":
                BOT.Options.unzip_pswd = temp_source[-1][1:-1]
                temp_source.pop()
            else:
                break

        BOT.SOURCE = temp_source
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Regular", callback_data="normal")],
                [
                    InlineKeyboardButton("Compress", callback_data="zip"),
                    InlineKeyboardButton("Extract", callback_data="unzip"),
                ],
                [InlineKeyboardButton("UnDoubleZip", callback_data="undzip")],
            ]
        )
        await message.reply_text(
            text=f"<b>🐹 Select Type of {BOT.Mode.mode.capitalize()} You Want » </b>\n\nRegular:<i> Normal file upload</i>\nCompress:<i> Zip file upload</i>\nExtract:<i> extract before upload</i>\nUnDoubleZip:<i> Unzip then compress</i>",
            reply_markup=keyboard,
            quote=True,
        )
    elif BOT.State.started:
        await message.delete()
        await message.reply_text(
            "<i>I am Already Working ! Please Wait Until I finish 😣!!</i>"
        )


@colab_bot.on_callback_query()
async def handle_options(client, callback_query):
    global BOT, MSG

    if callback_query.data in ["normal", "zip", "unzip", "undzip"]:
        BOT.Mode.type = callback_query.data
        await callback_query.message.delete()
        await colab_bot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id,
        )
        MSG.status_msg = await colab_bot.send_message(
            chat_id=OWNER,
            text="#STARTING_TASK\n\n**Starting your task in a few Seconds...🦐**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Cancel ❌", callback_data="cancel")],
                ]
            ),
        )
        BOT.State.task_going = True
        BOT.State.started = False
        BotTimes.start_time = datetime.now()
        event_loop = get_event_loop()
        BOT.TASK = event_loop.create_task(taskScheduler())  # type: ignore
        await BOT.TASK
        BOT.State.task_going = False

    elif callback_query.data == "video":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Split Videos", callback_data="split-true"),
                    InlineKeyboardButton("Zip Videos", callback_data="split-false"),
                ],
                [
                    InlineKeyboardButton("Convert", callback_data="convert-true"),
                    InlineKeyboardButton(
                        "Don't Convert", callback_data="convert-false"
                    ),
                ],
                [
                    InlineKeyboardButton("To » Mp4", callback_data="mp4"),
                    InlineKeyboardButton("To » Mkv", callback_data="mkv"),
                ],
                [
                    InlineKeyboardButton("High Quality", callback_data="q-High"),
                    InlineKeyboardButton("Low Quality", callback_data="q-Low"),
                ],
                [InlineKeyboardButton("Back ⏎", callback_data="back")],
            ]
        )
        await callback_query.message.edit_text(
            f"CHOOSE YOUR DESIRED OPTION ⚙️ »\n\n╭⌬ CONVERT » <code>{BOT.Setting.convert_video}</code>\n├⌬ SPLIT » <code>{BOT.Setting.split_video}</code>\n├⌬ OUTPUT FORMAT » <code>{BOT.Options.video_out}</code>\n╰⌬ OUTPUT QUALITY » <code>{BOT.Setting.convert_quality}</code>",
            reply_markup=keyboard,
        )
    elif callback_query.data == "caption":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Monospace", callback_data="code-Monospace"),
                    InlineKeyboardButton("Bold", callback_data="b-Bold"),
                ],
                [
                    InlineKeyboardButton("Italic", callback_data="i-Italic"),
                    InlineKeyboardButton("Underlined", callback_data="u-Underlined"),
                ],
                [InlineKeyboardButton("Regular", callback_data="p-Regular")],
            ]
        )
        await callback_query.message.edit_text(
            "CHOOSE YOUR CAPTION FONT STYLE »\n\n⌬ <code>Monospace</code>\n⌬ Regular\n⌬ <b>Bold</b>\n⌬ <i>Italic</i>\n⌬ <u>Underlined</u>",
            reply_markup=keyboard,
        )
    elif callback_query.data == "thumb":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Delete Thumbnail", callback_data="del-thumb"),
                ],
                [
                    InlineKeyboardButton("Go Back ⏎", callback_data="back"),
                ],
            ]
        )
        thmb_ = "None" if not BOT.Setting.thumbnail else "Exists"
        await callback_query.message.edit_text(
            f"CHOOSE YOUR THUMBNAIL SETTINGS »\n\n⌬ Thumbnail » {thmb_}\n⌬ Send an Image to set as Your Thumbnail",
            reply_markup=keyboard,
        )
    elif callback_query.data == "del-thumb":
        if BOT.Setting.thumbnail:
            os.remove(Paths.THMB_PATH)
        BOT.Setting.thumbnail = False
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data == "set-prefix":
        await callback_query.message.edit_text(
            "Send a Text to Set as PREFIX by REPLYING THIS MESSAGE »"
        )
        BOT.State.prefix = True
    elif callback_query.data == "set-suffix":
        await callback_query.message.edit_text(
            "Send a Text to Set as SUFFIX by REPLYING THIS MESSAGE »"
        )
        BOT.State.suffix = True
    elif callback_query.data in [
        "code-Monospace",
        "p-Regular",
        "b-Bold",
        "i-Italic",
        "u-Underlined",
    ]:
        res = callback_query.data.split("-")
        BOT.Options.caption = res[0]
        BOT.Setting.caption = res[1]
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data in ["split-true", "split-false"]:
        BOT.Options.is_split = True if callback_query.data == "split-true" else False
        BOT.Setting.split_video = (
            "Split Videos" if callback_query.data == "split-true" else "Zip Videos"
        )
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data in [
        "convert-true",
        "convert-false",
        "mp4",
        "mkv",
        "q-High",
        "q-Low",
    ]:
        if callback_query.data in ["convert-true", "convert-false"]:
            BOT.Options.convert_video = (
                True if callback_query.data == "convert-true" else False
            )
            BOT.Setting.convert_video = (
                "Yes" if callback_query.data == "convert-true" else "No"
            )
        elif callback_query.data in ["q-High", "q-Low"]:
            BOT.Setting.convert_quality = callback_query.data.split("-")[-1]
            BOT.Options.convert_quality = (
                True if BOT.Setting.convert_quality == "High" else False
            )
            await send_settings(
                client, callback_query.message, callback_query.message.id, False
            )
        else:
            BOT.Options.video_out = callback_query.data
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data in ["media", "document"]:
        BOT.Options.stream_upload = True if callback_query.data == "media" else False
        BOT.Setting.stream_upload = (
            "Media" if callback_query.data == "media" else "Document"
        )
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )

    elif callback_query.data == "close":
        await callback_query.message.delete()
    elif callback_query.data == "back":
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )

    # @main Triggering Actual Leech Functions
    elif callback_query.data in ["ytdl-true", "ytdl-false"]:
        BOT.Mode.ytdl = True if callback_query.data == "ytdl-true" else False
        await callback_query.message.delete()
        await colab_bot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id,
        )
        MSG.status_msg = await colab_bot.send_message(
            chat_id=OWNER,
            text="#STARTING_TASK\n\n**Starting your task in a few Seconds...🦐**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Cancel ❌", callback_data="cancel")],
                ]
            ),
        )
        BOT.State.task_going = True
        BOT.State.started = False
        BotTimes.start_time = datetime.now()
        event_loop = get_event_loop()
        BOT.TASK = event_loop.create_task(taskScheduler())  # type: ignore
        await BOT.TASK
        BOT.State.task_going = False

    # If user Wants to Stop The Task
    elif callback_query.data == "cancel":
        await cancelTask("User Cancelled !")


@colab_bot.on_message(filters.photo & filters.private)
async def handle_image(client, message):
    msg = await message.reply_text("<i>Trying To Save Thumbnail...</i>")
    success = await setThumbnail(message)
    if success:
        await msg.edit_text("**Thumbnail Successfully Changed ✅**")
        await message.delete()
    else:
        await msg.edit_text(
            "🥲 **Couldn't Set Thumbnail, Please Try Again !**", quote=True
        )
    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("setname") & filters.private)
async def custom_name(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/setname <code>custom_fileame.extension</code>\nTo Set Custom File Name 📛",
            quote=True,
        )
    else:
        BOT.Options.custom_name = message.command[1]
        msg = await message.reply_text(
            "Custom Name Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("zipaswd") & filters.private)
async def zip_pswd(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/zipaswd <code>password</code>\nTo Set Password for Output Zip File. 🔐",
            quote=True,
        )
    else:
        BOT.Options.zip_pswd = message.command[1]
        msg = await message.reply_text(
            "Zip Password Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("unzipaswd") & filters.private)
async def unzip_pswd(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/unzipaswd <code>password</code>\nTo Set Password for Extracting Archives. 🔓",
            quote=True,
        )
    else:
        BOT.Options.unzip_pswd = message.command[1]
        msg = await message.reply_text(
            "Unzip Password Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    msg = await message.reply_text(
        "Send /start To Check If I am alive 🤨\n\nSend /colabxr and follow prompts to start transloading 🚀\n\nSend /settings to edit bot settings ⚙️\n\nSend /setname To Set Custom File Name 📛\n\nSend /zipaswd To Set Password For Zip File 🔐\n\nSend /unzipaswd To Set Password to Extract Archives 🔓\n\nSend /premium To Enable 4GB Mode 🌟\n\n⚠️ **You can ALWAYS SEND an image To Set it as THUMBNAIL for your files 🌄**",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Instructions 📖",
                        url="https://github.com/M01K0/tl_script/wiki/INSTRUCTIONS",
                    ),
                ],
                [
                    InlineKeyboardButton(  # Opens a web URL
                        "Channel 📣",
                        url="https://t.me/Colab_Leecher",
                    ),
                    InlineKeyboardButton(  # Opens a web URL
                        "Group 💬",
                        url="https://t.me/Colab_Leecher_Discuss",
                    ),
                ],
            ]
        ),
    )
    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("premium") & filters.private)
async def toggle_premium(client, message):
    """Comando para activar/desactivar modo Premium 4GB"""
    global BOT
    
    # Verificar si existe session string
    session_file = "/content/tl_script/user_session.txt"
    
    try:
        if not os.path.exists(session_file):
            msg = await message.reply_text(
                "⚠️ **MODO PREMIUM NO DISPONIBLE**\n\n"
                "📋 **Para habilitar archivos de 4GB necesitas:**\n"
                "1. 📱 Generar tu session string de usuario\n"
                "2. 💳 Tener Telegram Premium activo\n\n"
                "🚀 **Pasos a seguir:**\n"
                "```\n"
                "!cd /content/tl_script && python3 generate_user_session.py\n"
                "```\n\n"
                "💡 **Después ejecuta** `/premium` **para activar**",
                quote=True
            )
            await sleep(20)
            await message_deleter(message, msg)
            return
        
        # Leer session string
        with open(session_file, 'r') as f:
            session_string = f.read().strip()
        
        if not session_string:
            msg = await message.reply_text(
                "❌ **Session string vacío o inválido**\n\n"
                "🔄 **Regenera tu session string:**\n"
                "```\n"
                "!cd /content/tl_script && python3 generate_user_session.py\n"
                "```",
                quote=True
            )
            await sleep(15)
            await message_deleter(message, msg)
            return
        
        # Alternar modo premium
        BOT.Options.premium_mode = not BOT.Options.premium_mode
        BOT.Options.user_session_string = session_string
        
        if BOT.Options.premium_mode:
            # Verificar si el usuario tiene Telegram Premium
            try:
                # Usar pyrofork directamente
                from pyrofork import Client
                user_client = Client(
                    "temp_premium_check",
                    api_id=colab_bot.api_id,
                    api_hash=colab_bot.api_hash,
                    session_string=session_string
                )
                await user_client.start()
                me = await user_client.get_me()
                is_premium = hasattr(me, 'is_premium') and me.is_premium
                await user_client.stop()
                
                BOT.Options.is_premium_user = is_premium
                BOT.Options.max_file_size = 4194304000 if is_premium else 2097152000  # 4GB o 2GB
                
                if is_premium:
                    status = "**🌟 MODO PREMIUM ACTIVADO**\n\n✅ Límite de archivos: **4GB**\n✅ Cliente de usuario habilitado\n✅ Soporte completo para Telegram Premium"
                else:
                    status = "**⚠️ MODO ACTIVADO - SIN PREMIUM**\n\n📋 Límite de archivos: **2GB**\n💡 Suscríbete a Telegram Premium para 4GB"
                    
            except Exception as e:
                BOT.Options.is_premium_user = False
                BOT.Options.max_file_size = 2097152000
                status = f"**❌ ERROR AL VERIFICAR PREMIUM**\n\n🔄 Session string válido pero error: {str(e)[:100]}...\n📋 Usando límite de 2GB por seguridad"
        else:
            BOT.Options.max_file_size = 2097152000   # 2GB
            BOT.Options.is_premium_user = False
            BOT.Options.user_session_string = ""
            status = "**📋 MODO ESTÁNDAR ACTIVADO**\n\n✅ Límite de archivos: **2GB**\n✅ División automática para archivos > 2GB"
        
        # Información adicional
        from colab_leecher import PYROFORK_AVAILABLE
        engine_status = "Pyrofork ✅" if PYROFORK_AVAILABLE else "Pyrogram ⚠️"
        max_theoretical = "4GB (Pyrofork ✅)" if PYROFORK_AVAILABLE else "2GB (Pyrogram ⚠️)"
        
        status += f"\n\n📊 **INFORMACIÓN TÉCNICA:**"
        status += f"\n▸ Motor: {engine_status}"
        status += f"\n▸ Máximo Teórico: {max_theoretical}"
        status += f"\n▸ Modo Premium: {'✅ Activado' if BOT.Options.premium_mode else '❌ Desactivado'}"
        status += f"\n▸ Límite Configurado: {BOT.Options.max_file_size // (1024*1024*1024)}GB"
        
        msg = await message.reply_text(status, quote=True)
        await sleep(25)
        await message_deleter(message, msg)
        
    except Exception as e:
        msg = await message.reply_text(
            f"❌ **ERROR EN COMANDO PREMIUM:**\n\n{str(e)}\n\n"
            "💡 **Intenta regenerar tu session string:**\n"
            "```\n"
            "!cd /content/tl_script && python3 generate_user_session.py\n"
            "```",
            quote=True
        )
        await sleep(20)
        await message_deleter(message, msg)


@colab_bot.on_message(filters.command("status") & filters.private)
async def status_command(client, message):
    """Comando para mostrar el estado actual del bot"""
    global BOT
    
    # Información del motor
    from colab_leecher import PYROFORK_AVAILABLE
    
    status_text = "**📊 ESTADO DEL BOT**\n\n"
    status_text += f"🔧 **Motor:** {'Pyrofork' if PYROFORK_AVAILABLE else 'Pyrogram'}\n"
    status_text += f"🌟 **Modo Premium:** {'✅ Activado' if BOT.Options.premium_mode else '❌ Desactivado'}\n"
    status_text += f"📊 **Límite Configurado:** {BOT.Options.max_file_size // (1024*1024*1024)}GB ({BOT.Options.max_file_size:,} bytes)\n"
    status_text += f"👤 **Usuario Premium:** {'✅ Detectado' if BOT.Options.is_premium_user else '❌ No detectado'}\n"
    status_text += f"🔑 **Session String:** {'✅ Disponible' if BOT.Options.user_session_string else '❌ No disponible'}\n"
    
    # Estado de tareas
    status_text += f"\n📋 **ESTADO DE TAREAS:**\n"
    status_text += f"▸ Bot Iniciado: {'✅ Sí' if BOT.State.started else '❌ No'}\n"
    status_text += f"▸ Tarea en Progreso: {'🚀 Sí' if BOT.State.task_going else '✅ Libre'}\n"
    
    # Configuración actual
    status_text += f"\n⚙️ **CONFIGURACIÓN:**\n"
    status_text += f"▸ Modo: {BOT.Mode.mode.capitalize()}\n"
    status_text += f"▸ Tipo: {BOT.Mode.type.capitalize()}\n"
    status_text += f"▸ Dividir Videos: {'✅' if BOT.Options.is_split else '❌'}\n"
    status_text += f"▸ Convertir Video: {'✅' if BOT.Options.convert_video else '❌'}\n"
    
    # Advertencias y recomendaciones
    LARGE_FILE_SUPPORT = PYROFORK_AVAILABLE
    if not LARGE_FILE_SUPPORT and BOT.Options.premium_mode:
        status_text += f"\n⚠️ **ADVERTENCIA:** Modo premium activado pero usando Pyrogram estándar\n"
        status_text += f"📝 **Recomendación:** Pyrofork ya está instalado, reinicia el bot\n"
    elif LARGE_FILE_SUPPORT and BOT.Options.premium_mode:
        status_text += f"\n🎉 **¡PERFECTO!** Configuración óptima para archivos de 4GB\n"
    
    msg = await message.reply_text(status_text, quote=True)
    await sleep(30)
    await message_deleter(message, msg)


logging.info("Colab Leecher Started !")
colab_bot.run()
