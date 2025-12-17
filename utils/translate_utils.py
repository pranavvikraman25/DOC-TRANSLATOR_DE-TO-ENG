from deep_translator import GoogleTranslator
import time

MAX_CHARS = 4500

# Simple in-memory cache
_translation_cache = {}

def chunk_text(text):
    chunks = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) < MAX_CHARS:
            current += line + "\n"
        else:
            chunks.append(current)
            current = line + "\n"

    if current.strip():
        chunks.append(current)

    return chunks


def translate_text(text):
    if not text.strip():
        return ""

    # 🔹 CACHE CHECK
    if text in _translation_cache:
        return _translation_cache[text]

    translator = GoogleTranslator(source="de", target="en")
    translated_chunks = []

    for chunk in chunk_text(text):
        try:
            translated_chunks.append(translator.translate(chunk))
            time.sleep(0.8)  # 🔑 THROTTLE (VERY IMPORTANT)
        except Exception:
            translated_chunks.append(chunk)  # fallback: show German

    result = "\n".join(translated_chunks)

    # 🔹 SAVE TO CACHE
    _translation_cache[text] = result
    return result
