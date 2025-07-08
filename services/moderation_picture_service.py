from schemas.moderation import MediaGroupResult, MediaItem, PicturePredictionResult, PicturePredicts
from helpers.nsfwCheck import nsfw_check
from helpers.utils import download_file, get_extension_from_url
from config.config import IMAGE_EXTENSIONS

def analyze_pictures(picture_urls):
    items = []
    for url in picture_urls:
        try:
            ext = get_extension_from_url(url, default=".jpg")
            if ext.lower() not in IMAGE_EXTENSIONS:
                raise ValueError(f"Unsupported image extension: {ext}")
            file_path = download_file(url, suffix=ext)
            raw = nsfw_check(file_path)
            prediction = PicturePredictionResult(
                path=raw["path"],
                isContainNude=raw["isContainNude"],
                isContainViolence=raw["isContainViolence"],
                predicts=PicturePredicts(
                    nude_score=raw["predicts"]["nude_score"],
                    violence_score=raw["predicts"]["violence_score"]
                )
            )
            items.append(MediaItem(source=url, predictions=prediction))
        except Exception as e:
            items.append(MediaItem(source=url, error=str(e)))

    return MediaGroupResult(field="pictures", results=items)
