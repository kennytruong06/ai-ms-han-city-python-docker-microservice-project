from schemas.moderation import ContentResult
from helpers.offensiveDetection import offensive_detection
import unicodedata

def analyze_texts(content_list):
    offensive_words = []
    for i, text in enumerate(content_list):
        if not isinstance(text, str):
            return ContentResult(field=f"content[{i}]", offensive_words=["Invalid type"])
        normalized = unicodedata.normalize('NFC', text.lower())
        offensive_words.extend(offensive_detection(normalized))

    return ContentResult(field="content", offensive_words=offensive_words)
