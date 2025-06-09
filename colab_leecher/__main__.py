# copyright 2024 © M01K0 | https://github.com/M01K0/tl_script


import logging, os, json
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
        "**🤖 COLAB LEECHER - GUÍA DE COMANDOS**\n\n"
        
        "**📁 COMANDOS BÁSICOS:**\n"
        "▸ `/start` - Verificar si el bot está activo 🔍\n"
        "▸ `/help` - Mostrar esta ayuda 📖\n"
        "▸ `/settings` - Configurar ajustes del bot ⚙️\n\n"
        
        "**🚀 COMANDOS DE SUBIDA:**\n"
        "▸ `/tupload` - Subir a Telegram 📤\n"
        "▸ `/gdupload` - Subir a Google Drive ☁️\n"
        "▸ `/ytupload` - Descargar de YouTube/YTDL 🎥\n"
        "▸ `/drupload` - Subir carpeta local 📁\n\n"
        
        "**🌟 MODO PREMIUM (4GB):**\n"
        "▸ `/premium` - Activar/desactivar modo 4GB 🌟\n"
        "▸ `/status` - Ver estado completo del bot 📊\n"
        "▸ `/diagnose` - Diagnóstico del sistema 🔍\n\n"
        
        "**🛠️ CONFIGURACIÓN:**\n"
        "▸ `/setname` - Nombre personalizado 📛\n"
        "▸ `/zipaswd` - Contraseña para ZIP 🔐\n"
        "▸ `/unzipaswd` - Contraseña para extraer 🔓\n\n"
        
        "**🌄 MINIATURA:**\n"
        "▸ **Envía una imagen** para usarla como thumbnail\n\n"
        
        "**🎯 PASOS PARA 4GB:**\n"
        "1. 💳 **Suscríbete a Telegram Premium**\n"
        "2. 🔑 **Genera session string:**\n"
        "   ```!cd /content/tl_script && python3 generate_user_session.py```\n"
        "3. 🌟 **Activa Premium:** `/premium`\n"
        "4. 📊 **Verifica estado:** `/status`\n"
        "5. 🧪 **Prueba con archivos >2GB**\n\n"
        
        "**🚨 SOLUCIÓN DE PROBLEMAS:**\n"
        "▸ Si no detecta Pyrofork: `/diagnose`\n"
        "▸ Si falla Premium: regenera session string\n"
        "▸ Para debug completo: `/status`",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📖 Instrucciones",
                        url="https://github.com/M01K0/tl_script/wiki/INSTRUCTIONS",
                    ),
                    InlineKeyboardButton(
                        "🔍 Session Generator",
                        url="https://github.com/M01K0/tl_script/blob/main/generate_user_session.py",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "📣 Canal",
                        url="https://t.me/Colab_Leecher",
                    ),
                    InlineKeyboardButton(
                        "💬 Grupo",
                        url="https://t.me/Colab_Leecher_Discuss",
                    ),
                ],
            ]
        ),
    )
    await sleep(20)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("premium") & filters.private)
async def toggle_premium(client, message):
    """🌟 Comando mejorado para activar/desactivar modo Premium 4GB - Similar a generate_user_session.py"""
    global BOT
    
    # Verificar si pyrofork está disponible (motor principal)
    if not BOT.Options.pyrofork_available:
        msg = await message.reply_text(
            "⚠️ **PYROFORK NO DISPONIBLE**\n\n"
            f"🔧 **Motor actual:** Pyrogram {BOT.Options.pyrogram_version}\n"
            f"📊 **Límite máximo:** 2GB\n\n"
            "🚀 **Para habilitar 4GB necesitas:**\n"
            "```\n"
            "pip install --force-reinstall pyrofork==2.2.11\n"
            "```\n\n"
            "🔄 **Después reinicia el bot** ejecutando main.py",
            quote=True
        )
        await sleep(20)
        await message_deleter(message, msg)
        return
    
    # Verificar si existe session string
    session_file = "/content/tl_script/user_session.txt"
    
    try:
        if not os.path.exists(session_file):
            msg = await message.reply_text(
                "⚠️ **SESSION STRING NO DISPONIBLE**\n\n"
                f"✅ **Pyrofork {BOT.Options.pyrogram_version} detectado correctamente**\n\n"
                "📋 **Para habilitar archivos de 4GB necesitas:**\n"
                "1. 📱 Generar tu session string de usuario\n"
                "2. 💳 Tener Telegram Premium activo\n\n"
                "🚀 **Ejecuta este comando:**\n"
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
            # 🔍 VERIFICACIÓN DE PREMIUM - Misma lógica que generate_user_session.py
            try:
                # Usar pyrofork directamente (disponible según detección mejorada)
                from pyrofork import Client
                
                temp_client = Client(
                    "temp_premium_check",
                    api_id=colab_bot.api_id,
                    api_hash=colab_bot.api_hash,
                    session_string=session_string
                )
                
                await temp_client.start()
                
                # Obtener información del usuario - misma detección que en tu script
                me = await temp_client.get_me()
                is_premium = hasattr(me, 'is_premium') and me.is_premium
                
                await temp_client.stop()
                
                # Configurar variables según detección
                BOT.Options.is_premium_user = is_premium
                BOT.Options.max_file_size = 4194304000 if is_premium else 2097152000  # 4GB o 2GB
                
                if is_premium:
                    status = "**🎉 MODO PREMIUM ACTIVADO EXITOSAMENTE**\n\n"
                    status += f"✅ **Usuario:** {me.first_name}\n"
                    if me.username:
                        status += f"✅ **Username:** @{me.username}\n"
                    status += f"✅ **Telegram Premium:** Detectado\n"
                    status += f"✅ **Límite de archivos:** 4GB\n"
                    status += f"✅ **Motor:** Pyrofork {BOT.Options.pyrogram_version}\n"
                    status += f"✅ **Cliente de usuario:** Habilitado\n\n"
                    status += "🚀 **Capacidades habilitadas:**\n"
                    status += "   ▸ Archivos de hasta 4GB\n"
                    status += "   ▸ Subida con cliente de usuario\n"
                    status += "   ▸ Soporte completo para Premium"
                else:
                    status = "**⚠️ MODO ACTIVADO - SIN TELEGRAM PREMIUM**\n\n"
                    status += f"👤 **Usuario:** {me.first_name}\n"
                    if me.username:
                        status += f"🔗 **Username:** @{me.username}\n"
                    status += f"❌ **Telegram Premium:** No detectado\n"
                    status += f"📋 **Límite de archivos:** 2GB (división automática)\n"
                    status += f"✅ **Motor:** Pyrofork {BOT.Options.pyrogram_version}\n\n"
                    status += "💡 **Para aprovechar 4GB:**\n"
                    status += "   1. 💳 Suscríbete a Telegram Premium\n"
                    status += "   2. 🔄 Ejecuta `/premium` nuevamente\n"
                    status += "   3. 🧪 Prueba subiendo archivos >2GB"
                    
            except ImportError:
                # Esto no debería pasar si la detección funciona bien
                BOT.Options.is_premium_user = False
                BOT.Options.max_file_size = 2097152000
                status = "❌ **ERROR CRÍTICO:** Pyrofork no disponible en tiempo de ejecución\n\n🔄 **Reinicia el bot**"
            except Exception as e:
                BOT.Options.is_premium_user = False
                BOT.Options.max_file_size = 2097152000
                status = f"**❌ ERROR AL VERIFICAR PREMIUM**\n\n"
                status += f"🔄 Session string válido pero error: {str(e)[:100]}...\n"
                status += f"📋 Usando límite de 2GB por seguridad\n\n"
                status += f"💡 **Soluciones posibles:**\n"
                status += f"   1. 🔄 Regenera session string\n"
                status += f"   2. ✅ Verifica conexión a internet\n"
                status += f"   3. 🔑 Revisa credenciales de API"
        else:
            BOT.Options.max_file_size = 2097152000   # 2GB
            BOT.Options.is_premium_user = False
            BOT.Options.user_session_string = ""
            BOT.Options.user_client_active = False
            status = "**📋 MODO ESTÁNDAR ACTIVADO**\n\n"
            status += "✅ Límite de archivos: **2GB**\n"
            status += "✅ División automática para archivos > 2GB\n"
            status += "✅ Cliente bot estándar\n"
            status += f"✅ Motor: Pyrofork {BOT.Options.pyrogram_version}"
        
        # 📊 INFORMACIÓN TÉCNICA DETALLADA
        status += f"\n\n📊 **INFORMACIÓN TÉCNICA:**"
        status += f"\n▸ **Motor detectado:** Pyrofork {BOT.Options.pyrogram_version} ✅"
        status += f"\n▸ **Soporte 4GB:** ✅ Disponible"
        status += f"\n▸ **Modo Premium:** {'✅ Activado' if BOT.Options.premium_mode else '❌ Desactivado'}"
        status += f"\n▸ **Session String:** {'✅ Cargado' if BOT.Options.user_session_string else '❌ No disponible'}"
        status += f"\n▸ **Límite configurado:** {BOT.Options.max_file_size // (1024*1024*1024)}GB"
        status += f"\n▸ **Archivos grandes:** {'Cliente Usuario' if BOT.Options.is_premium_user else 'Cliente Bot'}"
        
        msg = await message.reply_text(status, quote=True)
        await sleep(30)
        await message_deleter(message, msg)
        
    except Exception as e:
        msg = await message.reply_text(
            f"❌ **ERROR EN COMANDO PREMIUM:**\n\n{str(e)}\n\n"
            "💡 **Soluciones:**\n"
            "1. 🔄 Regenera session string:\n"
            "```\n"
            "!cd /content/tl_script && python3 generate_user_session.py\n"
            "```\n"
            "2. ✅ Verifica credenciales en main.py\n"
            "3. 🔄 Reinicia el bot si es necesario",
            quote=True
        )
        await sleep(20)
        await message_deleter(message, msg)


@colab_bot.on_message(filters.command("status") & filters.private)
async def status_command(client, message):
    """📊 Comando mejorado para mostrar el estado completo del bot"""
    global BOT
    
    # Verificar disponibilidad de session string
    session_file = "/content/tl_script/user_session.txt"
    session_available = os.path.exists(session_file)
    
    # 🚀 ENCABEZADO PRINCIPAL
    status_text = "**📊 ESTADO COMPLETO DEL BOT**\n"
    status_text += "=" * 35 + "\n\n"
    
    # 🔧 INFORMACIÓN DEL MOTOR
    status_text += "🔧 **MOTOR Y CAPACIDADES:**\n"
    if BOT.Options.pyrofork_available:
        status_text += f"▸ **Librería:** Pyrofork {BOT.Options.pyrogram_version} ✅\n"
        status_text += f"▸ **Soporte 4GB:** ✅ Disponible\n"
        status_text += f"▸ **Optimización:** ✅ Archivos grandes\n"
    else:
        status_text += f"▸ **Librería:** Pyrogram {BOT.Options.pyrogram_version} ⚠️\n"
        status_text += f"▸ **Soporte 4GB:** ❌ No disponible\n"
        status_text += f"▸ **Límite máximo:** 2GB estándar\n"
    
    # 🌟 ESTADO PREMIUM
    status_text += "\n🌟 **MODO PREMIUM:**\n"
    status_text += f"▸ **Estado:** {'✅ Activado' if BOT.Options.premium_mode else '❌ Desactivado'}\n"
    status_text += f"▸ **Usuario Premium:** {'✅ Detectado' if BOT.Options.is_premium_user else '❌ No detectado'}\n"
    status_text += f"▸ **Session String:** {'✅ Disponible' if session_available else '❌ No encontrado'}\n"
    status_text += f"▸ **Cliente Usuario:** {'✅ Activo' if BOT.Options.user_client_active else '❌ Inactivo'}\n"
    
    # 📊 LÍMITES DE ARCHIVOS
    current_limit_gb = BOT.Options.max_file_size // (1024*1024*1024)
    status_text += f"\n📊 **LÍMITES DE ARCHIVOS:**\n"
    status_text += f"▸ **Límite configurado:** {current_limit_gb}GB ({BOT.Options.max_file_size:,} bytes)\n"
    
    if BOT.Options.premium_mode and BOT.Options.is_premium_user:
        status_text += f"▸ **Tipo de subida:** Cliente Usuario (4GB)\n"
        status_text += f"▸ **Archivos grandes:** ✅ Soportados\n"
    elif BOT.Options.premium_mode and not BOT.Options.is_premium_user:
        status_text += f"▸ **Tipo de subida:** Cliente Bot (2GB + división)\n"
        status_text += f"▸ **División automática:** ✅ Para archivos >2GB\n"
    else:
        status_text += f"▸ **Tipo de subida:** Cliente Bot estándar\n"
        status_text += f"▸ **División automática:** ✅ Para archivos >2GB\n"
    
    # 📋 ESTADO DE TAREAS
    status_text += f"\n📋 **ESTADO DE TAREAS:**\n"
    status_text += f"▸ **Bot iniciado:** {'✅ Sí' if BOT.State.started else '❌ No'}\n"
    status_text += f"▸ **Tarea activa:** {'🚀 En progreso' if BOT.State.task_going else '✅ Libre'}\n"
    status_text += f"▸ **Modo actual:** {BOT.Mode.mode.capitalize()}\n"
    status_text += f"▸ **Tipo de proceso:** {BOT.Mode.type.capitalize()}\n"
    
    # ⚙️ CONFIGURACIÓN AVANZADA
    status_text += f"\n⚙️ **CONFIGURACIÓN:**\n"
    status_text += f"▸ **Dividir videos:** {'✅ Activado' if BOT.Options.is_split else '❌ Desactivado'}\n"
    status_text += f"▸ **Convertir video:** {'✅ Activado' if BOT.Options.convert_video else '❌ Desactivado'}\n"
    status_text += f"▸ **Formato salida:** {BOT.Options.video_out.upper()}\n"
    status_text += f"▸ **Calidad:** {'Baja' if not BOT.Options.convert_quality else 'Alta'}\n"
    
    # 🎯 RECOMENDACIONES Y ADVERTENCIAS
    status_text += f"\n🎯 **RECOMENDACIONES:**\n"
    
    if not BOT.Options.pyrofork_available:
        status_text += f"⚠️ **Instala Pyrofork para 4GB:**\n"
        status_text += f"   ```pip install --force-reinstall pyrofork==2.2.11```\n"
    elif BOT.Options.pyrofork_available and not session_available:
        status_text += f"💡 **Genera session string para Premium:**\n"
        status_text += f"   ```!cd /content/tl_script && python3 generate_user_session.py```\n"
    elif BOT.Options.pyrofork_available and session_available and not BOT.Options.premium_mode:
        status_text += f"🌟 **Activa modo Premium:**\n"
        status_text += f"   Ejecuta: `/premium`\n"
    elif BOT.Options.premium_mode and BOT.Options.is_premium_user:
        status_text += f"🎉 **¡Configuración perfecta!** Todo listo para 4GB\n"
    else:
        status_text += f"✅ **Sistema funcionando correctamente**\n"
    
    # 🔍 INFORMACIÓN TÉCNICA DE DEBUG
    status_text += f"\n🔍 **INFORMACIÓN TÉCNICA:**\n"
    status_text += f"▸ **Pyrofork disponible:** {'✅' if BOT.Options.pyrofork_available else '❌'}\n"
    status_text += f"▸ **Versión librería:** {BOT.Options.pyrogram_version}\n"
    status_text += f"▸ **Umbral archivos grandes:** {BOT.Options.large_file_threshold // (1024*1024)}MB\n"
    status_text += f"▸ **Session cargado:** {'✅' if BOT.Options.user_session_string else '❌'}\n"
    
    msg = await message.reply_text(status_text, quote=True)
    await sleep(35)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("diagnose") & filters.private)
async def diagnose_system(client, message):
    """🔍 Comando de diagnóstico avanzado para detectar problemas de configuración"""
    global BOT
    
    # 🔍 INICIO DEL DIAGNÓSTICO
    msg_text = "**🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA**\n"
    msg_text += "=" * 40 + "\n\n"
    
    # 📦 VERIFICAR INSTALACIONES
    msg_text += "📦 **VERIFICACIÓN DE LIBRERÍAS:**\n"
    
    try:
        import pyrofork
        msg_text += f"✅ **Pyrofork:** {pyrofork.__version__} (Instalado)\n"
        pyrofork_installed = True
    except ImportError:
        msg_text += f"❌ **Pyrofork:** No instalado\n"
        pyrofork_installed = False
    
    try:
        import pyrogram
        msg_text += f"✅ **Pyrogram:** {pyrogram.__version__} (Disponible)\n"
    except ImportError:
        msg_text += f"❌ **Pyrogram:** No disponible\n"
    
    # 🔧 ESTADO DE LA DETECCIÓN
    msg_text += f"\n🔧 **ESTADO DE DETECCIÓN:**\n"
    msg_text += f"▸ **BOT.Options.pyrofork_available:** {BOT.Options.pyrofork_available}\n"
    msg_text += f"▸ **BOT.Options.pyrogram_version:** {BOT.Options.pyrogram_version}\n"
    msg_text += f"▸ **Detección vs Instalación:** {'✅ Coincide' if BOT.Options.pyrofork_available == pyrofork_installed else '❌ NO COINCIDE'}\n"
    
    # 📁 VERIFICAR ARCHIVOS
    msg_text += f"\n📁 **VERIFICACIÓN DE ARCHIVOS:**\n"
    
    # Verificar credentials.json
    credentials_file = "/content/tl_script/credentials.json"
    if os.path.exists(credentials_file):
        msg_text += f"✅ **credentials.json:** Existe\n"
        try:
            with open(credentials_file, 'r') as f:
                creds = json.loads(f.read())
                msg_text += f"   ▸ API_ID: {'✅ Configurado' if creds.get('API_ID') else '❌ Vacío'}\n"
                msg_text += f"   ▸ API_HASH: {'✅ Configurado' if creds.get('API_HASH') else '❌ Vacío'}\n"
                msg_text += f"   ▸ BOT_TOKEN: {'✅ Configurado' if creds.get('BOT_TOKEN') else '❌ Vacío'}\n"
        except Exception as e:
            msg_text += f"   ❌ Error leyendo: {str(e)[:50]}...\n"
    else:
        msg_text += f"❌ **credentials.json:** No existe\n"
    
    # Verificar user_session.txt
    session_file = "/content/tl_script/user_session.txt"
    if os.path.exists(session_file):
        msg_text += f"✅ **user_session.txt:** Existe\n"
        try:
            with open(session_file, 'r') as f:
                session_content = f.read().strip()
                msg_text += f"   ▸ Contenido: {'✅ No vacío' if session_content else '❌ Vacío'}\n"
                msg_text += f"   ▸ Longitud: {len(session_content)} caracteres\n"
        except Exception as e:
            msg_text += f"   ❌ Error leyendo: {str(e)[:50]}...\n"
    else:
        msg_text += f"❌ **user_session.txt:** No existe\n"
    
    # 🌟 VERIFICAR CONFIGURACIÓN PREMIUM
    msg_text += f"\n🌟 **CONFIGURACIÓN PREMIUM:**\n"
    msg_text += f"▸ **premium_mode:** {BOT.Options.premium_mode}\n"
    msg_text += f"▸ **is_premium_user:** {BOT.Options.is_premium_user}\n"
    msg_text += f"▸ **user_session_string:** {'✅ Cargado' if BOT.Options.user_session_string else '❌ Vacío'}\n"
    msg_text += f"▸ **user_client_active:** {BOT.Options.user_client_active}\n"
    msg_text += f"▸ **max_file_size:** {BOT.Options.max_file_size:,} bytes ({BOT.Options.max_file_size // (1024*1024*1024)}GB)\n"
    
    # 🚨 PROBLEMAS DETECTADOS
    msg_text += f"\n🚨 **PROBLEMAS DETECTADOS:**\n"
    problems = []
    
    if not pyrofork_installed:
        problems.append("Pyrofork no está instalado")
    if BOT.Options.pyrofork_available != pyrofork_installed:
        problems.append("Discrepancia en detección de Pyrofork")
    if not os.path.exists(credentials_file):
        problems.append("Archivo credentials.json no existe")
    if BOT.Options.premium_mode and not BOT.Options.user_session_string:
        problems.append("Modo Premium activado sin session string")
    
    if problems:
        for i, problem in enumerate(problems, 1):
            msg_text += f"   {i}. ❌ {problem}\n"
    else:
        msg_text += f"   🎉 **¡No se detectaron problemas!**\n"
    
    # 💊 SOLUCIONES RECOMENDADAS
    msg_text += f"\n💊 **SOLUCIONES RECOMENDADAS:**\n"
    
    if not pyrofork_installed:
        msg_text += f"1. 📦 **Instalar Pyrofork:**\n"
        msg_text += f"   ```pip install --force-reinstall pyrofork==2.2.11```\n"
    
    if not os.path.exists(session_file) and pyrofork_installed:
        msg_text += f"2. 🔑 **Generar Session String:**\n"
        msg_text += f"   ```!cd /content/tl_script && python3 generate_user_session.py```\n"
    
    if pyrofork_installed and os.path.exists(session_file) and not BOT.Options.premium_mode:
        msg_text += f"3. 🌟 **Activar Modo Premium:**\n"
        msg_text += f"   Ejecuta: `/premium`\n"
    
    msg_text += f"\n🔄 **Después de las correcciones:**\n"
    msg_text += f"   1. Reinicia el bot ejecutando main.py\n"
    msg_text += f"   2. Ejecuta `/status` para verificar\n"
    msg_text += f"   3. Prueba `/diagnose` nuevamente\n"
    
    msg = await message.reply_text(msg_text, quote=True)
    await sleep(45)
    await message_deleter(message, msg)


logging.info("Colab Leecher Started !")
colab_bot.run()
