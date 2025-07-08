import os
from config.config import TEMP_DIR

def cleanup_file_temp():
    for filename in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, filename))
        except:
            pass
