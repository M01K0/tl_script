# copyright 2023 © M01K0 | https://github.com/M01K0/tl_script


from time import time
from datetime import datetime
from pyrogram.types import Message


class BOT:
    SOURCE = []
    TASK = None
    class Setting:
        stream_upload = "Media"
        convert_video = "Yes"
        convert_quality = "Low"
        caption = "Monospace"
        split_video = "Split Videos"
        prefix = ""
        suffix = ""
        thumbnail = False

    class Options:
        stream_upload = True
        convert_video = True
        convert_quality = False
        is_split = True
        caption = "code"
        video_out = "mp4"
        custom_name = ""
        zip_pswd = ""
        unzip_pswd = ""
        # Variables para soporte Premium y límites dinámicos
        max_file_size = 2097152000  # 2GB inicial - se reconfigura a 4GB si Premium
        premium_mode = False
        user_session_string = ""
        is_premium_user = False
        large_file_threshold = 2097152000  # 2GB inicial - umbral para cambiar a cliente usuario
        # 🆕 NUEVAS VARIABLES PARA DETECCIÓN MEJORADA
        pyrofork_available = False  # Se configura en __init__.py
        pyrogram_version = "unknown"  # Versión detectada de la librería
        # Variables de estado del cliente usuario
        user_client_active = False
        user_client_instance = None

    class Mode:
        mode = "leech"
        type = "normal"
        ytdl = False

    class State:
        started = False
        task_going = False
        prefix = False
        suffix = False


class YTDL:
    header = ""
    speed = ""
    percentage = 0.0
    eta = ""
    done = ""
    left = ""


class Transfer:
    down_bytes = [0, 0]
    up_bytes = [0, 0]
    total_down_size = 0
    sent_file = []
    sent_file_names = []


class TaskError:
    state = False
    text = ""


class BotTimes:
    current_time = time()
    start_time = datetime.now()
    task_start = datetime.now()


class Paths:
    WORK_PATH = "/content/tl_script/BOT_WORK"
    THMB_PATH = "/content/tl_script/colab_leecher/Thumbnail.jpg"
    VIDEO_FRAME = f"{WORK_PATH}/video_frame.jpg"
    HERO_IMAGE = f"{WORK_PATH}/Hero.jpg"
    DEFAULT_HERO =  "/content/tl_script/custom_thmb.jpg"
    MOUNTED_DRIVE = "/content/drive"
    down_path = f"{WORK_PATH}/Downloads"
    temp_dirleech_path = f"{WORK_PATH}/dir_leech_temp"
    mirror_dir = "/content/drive/MyDrive/Colab Leecher Uploads"
    temp_zpath = f"{WORK_PATH}/Leeched_Files"
    temp_unzip_path = f"{WORK_PATH}/Unzipped_Files"
    temp_files_dir = f"{WORK_PATH}/leech_temp"
    thumbnail_ytdl = f"{WORK_PATH}/ytdl_thumbnails"
    access_token = "/content/token.pickle"


class Messages:
    caution_msg = "\n\n<i>💖 When I'm Doin This, Do Something Else ! <b>Because, Time Is Precious ✨</b></i>"
    download_name = ""
    task_msg = ""
    status_head = f"<b>📥 DOWNLOADING » </b>\n"
    dump_task = ""
    src_link = ""
    link_p = ""


class MSG:
    sent_msg = Message(id=1)
    status_msg = Message(id=2)



class Aria2c:
    link_info = False
    pic_dwn_url = "https://picsum.photos/900/600"


class Gdrive:
    service = None
