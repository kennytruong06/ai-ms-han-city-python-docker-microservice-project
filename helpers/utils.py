from urllib.parse import urlparse
from config.config import TEMP_DIR, REQUEST_TIMEOUT, MAX_DOWNLOAD_SIZE_MB
import os
import uuid
import requests
import shutil

def get_extension_from_url(url: str, default=".dat") -> str:
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext if ext else default

def download_file(url: str, suffix=".dat") -> str:
    uid = str(uuid.uuid4())[:8]
    file_path = os.path.join(TEMP_DIR, f"{uid}{suffix}")

    if url.startswith("http"):
        response = requests.get(url, stream=True, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        total_bytes = 0
        max_bytes = MAX_DOWNLOAD_SIZE_MB * 1024 * 1024
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    total_bytes += len(chunk)
                    if total_bytes > max_bytes:
                        f.close()
                        os.remove(file_path)
                        raise ValueError(f"File too large (> {MAX_DOWNLOAD_SIZE_MB}MB): {url}")
                    f.write(chunk)
    else:
        if not os.path.isfile(url):
            raise FileNotFoundError(f"Local file not found: {url}")
        shutil.copy(url, file_path)

    return file_path
