from deep_translator import GoogleTranslator

MAX_CHARS = 4500  # safe limit

def chunk_text(text, max_chars=MAX_CHARS):
    chunks = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) < max_chars:
            current += line + "\n"
        else:
            chunks.append(current)
            current = line + "\n"

    if current:
        chunks.append(current)

    return chunks


def translate_text(text):
    translator = GoogleTranslator(source="de", target="en")
    chunks = chunk_text(text)

    translated_chunks = []
    for chunk in chunks:
        translated_chunks.append(translator.translate(chunk))

    return "\n".join(translated_chunks)
