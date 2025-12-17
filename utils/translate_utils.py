from deep_translator import GoogleTranslator

MAX_CHARS = 4500

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
    translator = GoogleTranslator(source="de", target="en")
    translated_chunks = []

    for chunk in chunk_text(text):
        translated_chunks.append(translator.translate(chunk))

    return "\n".join(translated_chunks)
