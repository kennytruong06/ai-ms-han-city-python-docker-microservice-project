from schemas.moderation import MediaGroupResult, MediaItem, VideoPredictionResult
from helpers.nsfwCheck import nsfw_check_video
from helpers.utils import download_file, get_extension_from_url
from config.config import VIDEO_EXTENSIONS, DEFAULT_FRAME_SKIP

def analyze_videos(video_urls):
    items = []
    for url in video_urls:
        try:
            ext = get_extension_from_url(url, default=".mp4")

            if ext.lower() not in VIDEO_EXTENSIONS:
                raise ValueError(f"Unsupported video extension: {ext}")

            file_path = download_file(url, suffix=ext)
            raw = nsfw_check_video(file_path, frame_skip=DEFAULT_FRAME_SKIP)
            prediction = VideoPredictionResult(
                path=raw["path"],
                type=raw["type"],
                timestamps=raw["timestamps"]
            )
            items.append(MediaItem(source=url, predictions=prediction))

            if "NSFW content" in raw["type"]:
                return MediaGroupResult(field="videos", results=items)
        except Exception as e:
            items.append(MediaItem(source=url, error=str(e)))

    return MediaGroupResult(field="videos", results=items)
