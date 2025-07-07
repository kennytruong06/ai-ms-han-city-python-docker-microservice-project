import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMP_DIR = os.path.join(ROOT_DIR, "storage", "downloaded")
os.makedirs(TEMP_DIR, exist_ok=True)

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')

VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv', '.webm')

MAX_DOWNLOAD_SIZE_MB = 100

REQUEST_TIMEOUT = (5, 60)

DEFAULT_FRAME_SKIP = 30
